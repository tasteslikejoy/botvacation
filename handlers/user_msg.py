from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards import reply
from extensions import dbcreate

router = Router()


# обработка команды /start
@router.message(CommandStart())
async def start_command(message:Message):
    # Вызывает асинхронную функцию для инициализации базы данных.
    await dbcreate.init_db()
    # Из объекта message извлекается идентификатор пользователя (чата), который отправил команду
    chat_id = message.from_user.id
    try:
        # Эта строка вызывает асинхронную функцию для создания нового пользователя в базе данных, используя его chat_id
        await dbcreate.create_user(chat_id)
        await message.answer(f'Привет, {message.from_user.username}!', reply_markup=reply.main_kb)
    except Exception as e:
        await message.answer(f'Ошибка: {e}')

