import asyncio

from prometheus_client import Summary, start_http_server

from monitox.bot import bot, dp, logger
from monitox.commands import set_commands
from monitox.handlers import router

REQUEST_TIME = Summary("request_processing_seconds", "Time spent processing request")


async def main():
    start_http_server(8001)

    dp.include_router(router)
    dp.startup.register(set_commands)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
