import asyncio
import psutil
from prometheus_client import start_http_server, Summary, Gauge

from monitox.bot import bot, dp, logger, memory_usage, cpu_usage
from monitox.commands import set_commands
from monitox.handlers import router

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

async def update_system_metrics():
    while True:
        memory_usage.set(psutil.virtual_memory().used)
        cpu_usage.set(psutil.cpu_percent()) 
        await asyncio.sleep(5)

async def main():
    start_http_server(8001)

    asyncio.create_task(update_system_metrics())

    dp.include_router(router)
    dp.startup.register(set_commands)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")