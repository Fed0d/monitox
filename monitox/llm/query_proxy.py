import logging
from pathlib import Path

import requests
from mistralai import Mistral
from orjson import JSONDecodeError, orjson

from monitox.llm.data import (
    AnalysisResponse,
    VulnerabilityRequest,
    VulnerabilityResponse,
)
from monitox.models import Query, Session, ToxicityAnalysis, VulnerabilityAnalysis
from monitox.settings import config

root = Path(__name__).parent.parent / "prompts" / "system" / "toxic_detecting"
with root.open("r") as system_prompt_file:
    system_prompt = system_prompt_file.read()

client = Mistral(api_key=config.llm.mistral.api_key)
vulnerability_url = config.vulnerability.vulnerability_url


def process_query(user_id: int, user_query: str) -> str:
    with Session() as session:
        query = Query(
            request=user_query,
            user_id=user_id,
            llm=config.llm.mistral.model,
        )
        session.add(query)
        session.commit()

        vulnerability_request = VulnerabilityRequest(text=user_query).model_dump()
        vulnerability_response = requests.post(
            vulnerability_url, json=vulnerability_request
        )

        if vulnerability_response.status_code != 200:
            return "No answer"

        vulnerability_response = VulnerabilityResponse(**vulnerability_response.json())
        max_key = max(
            vulnerability_response.model_dump(),
            key=vulnerability_response.model_dump().get,
        )

        flagged = True if max_key != "benign" else False

        vulnerability_analysis = VulnerabilityAnalysis(
            query_id=query.id,
            flagged=flagged,
            **vulnerability_response.model_dump(),
        )
        session.add(vulnerability_analysis)

        if flagged:
            session.commit()
            return "It seems that this prompt is trying to exploit my vulnerabilities!"

        chat_session = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query},
            ]
        }
        chat_response = client.chat.complete(
            model=config.llm.mistral.model,
            messages=chat_session["messages"],
        )

        raw_response = chat_response.choices[0].message.content
        if raw_response:
            try:
                json_response = orjson.loads(raw_response)
                response = AnalysisResponse(**json_response)
            except JSONDecodeError as e:
                logging.error(e)
                return "Model mad crazy!"

            toxicity_analysis = ToxicityAnalysis(
                query_id=query.id,
                flagged=response.toxicity_analysis.flagged,
                **orjson.loads(response.toxicity_analysis.categories.model_dump_json()),
            )

            session.add(toxicity_analysis)
            session.commit()

            return response.answer
    return "No answer"
