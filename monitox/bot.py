import logging
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from monitox.settings import config
from monitox.prometheus import llm_requests_total, llm_errors_total, track_llm_request_duration

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

bot = Bot(config.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

async def send_request_to_llm(prompt: str) -> str:
    llm_url = config.llm.mistral.api_key  
    headers = {
        'Authorization': f'Bearer {config.llm.mistral.api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        "prompt": prompt,
        "model": config.llm.mistral.model 
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(llm_url, json=payload, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get("response", "Нет ответа")
    except Exception as e:
        logger.error(f"Ошибка при отправке запроса к LLM: {e}")
        raise

async def process_llm_request(prompt: str):
    llm_requests_total.inc() 
    try:
        result = await track_llm_request_duration(send_request_to_llm, prompt)
    except Exception as e:
        llm_errors_total.inc()  
        logger.error(f"LLM request failed: {e}")
        return None
    return result
