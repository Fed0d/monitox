import logging
from pathlib import Path

from mistralai import Mistral
from orjson import JSONDecodeError, orjson  # type: ignore[attr-defined]

from monitox.llm.data import AnalysisResponse
from monitox.models import Query, Session, ToxicityAnalysis
from monitox.settings import config

root = Path(__name__).parent.parent / "prompts" / "system" / "toxic_detecting"
with root.open("r") as system_prompt_file:
    system_prompt = system_prompt_file.read()

client = Mistral(api_key=config.llm.mistral.api_key)


def process_query(user_id: int, user_query: str) -> str:
    session = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query},
        ]
    }
    chat_response = client.chat.complete(
        model=config.llm.mistral.model,
        messages=session["messages"],
    )

    raw_response = chat_response.choices[0].message.content
    if raw_response:
        try:
            json_response = orjson.loads(raw_response)
            response = AnalysisResponse(**json_response)
        except JSONDecodeError as e:
            logging.error(e)
            return "Model mad crazy!"
        with Session() as session:
            query = Query(
                request=user_query,
                user_id=user_id,
                llm=config.llm.mistral.model,
            )
            session.add(query)

            toxicity_analysis = ToxicityAnalysis(
                flagged=response.toxicity_analysis.flagged,
                **orjson.loads(response.toxicity_analysis.categories.model_dump_json()),
            )

            session.add(toxicity_analysis)
            session.commit()

        return response.answer
    return "No answer"
