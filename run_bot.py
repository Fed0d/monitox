import asyncio
from monitox.bot import bot, dp, logger
from monitox.commands import set_commands
from monitox.handlers import router

async def main():
    dp.include_router(router)
    dp.startup.register(set_commands)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
