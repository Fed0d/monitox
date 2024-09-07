from aiogram.types import BotCommand, BotCommandScopeDefault

from monitox.bot import bot

commands = [
    BotCommand(command="start", description="Запуск бота"),
    BotCommand(command="help", description="Помощь"),
    BotCommand(command="settings", description="Настройки"),
    BotCommand(command="start_dialog", description="Начать диалог"),
    BotCommand(command="stop_dialog", description="Остановить диалог"),
]


async def set_commands():
    await bot.set_my_commands(commands, BotCommandScopeDefault())
