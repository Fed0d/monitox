import asyncio
from prometheus_client import start_http_server, Summary
from monitox.bot import bot, dp, logger
from monitox.commands import set_commands
from monitox.handlers import router
from monitox.metrics import update_system_metrics
from monitox.settings import config  

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

async def main():
    start_http_server(config.metrics.port)
    asyncio.create_task(update_system_metrics())

    dp.include_router(router)
    dp.startup.register(set_commands)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")