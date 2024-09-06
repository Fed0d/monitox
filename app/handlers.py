from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
import app.keyboards as kb

router = Router()

class Dialog(StatesGroup):
    dialog = State()

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('Привет!\n'
                        'Я - бот, который отвечает на вопросы.', reply_markup=kb.start)

@router.message(Command('help'))
@router.message(F.text  == kb.button_texts['help'])
async def process_help(message: Message):
    await message.answer('Помощь пока недоступна.')

@router.message(Command('start_dialog'))
@router.message(F.text == kb.button_texts['start_dialog'])
async def start_dialog(message: Message, state: FSMContext):
    await message.answer('Начинаем диалог.', reply_markup=kb.stop_dialog)
    await state.set_state(Dialog.dialog)

@router.message(Command('stop_dialog'))
@router.message(F.text == kb.button_texts['stop_dialog'])
async def stop_dialog(message: Message, state: FSMContext):
    await message.answer('Диалог завершён.', reply_markup=kb.start)
    await state.clear()

@router.message(Dialog.dialog)
async def process_dialog(message: Message):
    await message.answer('Я не знаю, что ответить. Попробуйте задать другой вопрос.')
