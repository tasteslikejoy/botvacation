from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards import reply
from extensions import dbcreate


# Используется для организации маршрутов в боте.
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
        await message.answer(f'Привет, {message.from_user.username}!👋👋👋\n'
                             f'Я ваш бот помощник! Вот, что вы сможете делать:\n'
                             f'\n'
                             f'Добавлять записи в свой ежедневник 📔\n'
                             f'Так же вы можете редактировать и удалять их! Я запомню все!\n'
                             f'\n'
                             f'Можно создавать задачи, о которых я тебе напомню 🕚\n'
                             f'\n'
                             f'Так же могу помочь тебе собрать вещи, что бы ты ничего не забыл!\n'
                             f'Вместе у нас получится провести незабываемый отпуск! 🌅🍹'
                             f'', reply_markup=reply.main_kb)
    except Exception as e:
        await message.answer(f'Ошибка: {e}')

