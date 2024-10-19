from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.states import Formtime
from keyboards import reply
from extensions import dbcreate


# Используется для организации маршрутов в боте.
router = Router()


# Этот обработчик активируется, когда пользователь отправляет сообщение с текстом 'создать задачу' или 'запланировать отдых'
@router.message(F.text.lower().in_(['создать задачу', 'запланировать отдых']))
async def process_message(message: Message, state: FSMContext):
    # Состояние FSM устанавливается в Formtime.note, что указывает на ожидание ввода напоминания
    await state.set_state(Formtime.note)
    await message.answer('Введите текст напоминания:', reply_markup=reply.call_kb)


# Этот обработчик активируется, когда пользователь вводит текст
@router.message(Formtime.note)
async def form_class(message: Message, state: FSMContext):
    # Текст напоминания сохраняется в состоянии FSM
    await state.update_data(note=message.text)
    # Бот переводит состояние в Formtime.time, ожидая ввод даты и времени
    await state.set_state(Formtime.time)
    await message.answer('Введите дату и время в формате: "YYYY-MM-DD HH:MM".\n'
                         'Например: 2013-10-14 10:00', reply_markup=reply.call_kb)


# В этом обработчике ожидается ввод даты и времени
@router.message(Formtime.time)
async def process_time(message: Message, state: FSMContext):
    # Введенное значение обрезается с помощью strip(), чтобы убрать лишние пробелы
    time_input = message.text.strip()

    try:
        # Программа пытается преобразовать строку во временной объект с помощью strptime
        date_time = datetime.strptime(time_input, '%Y-%m-%d %H:%M')

        # Проверяется, что введенное время не находится в прошлом
        if date_time < datetime.now():
            await message.answer('Время не может быть в прошлом. Пожалуйста, введите дату и время в будущем.')
            return

        # Извлекается текст напоминания из состояния FSM, и если оно пустое, появляется соответствующее сообщение
        data = await state.get_data()
        diary_content = data.get('note')

        if not diary_content or diary_content.strip() == "":
            await message.answer('Содержимое напоминания не может быть пустым. Пожалуйста, введите текст напоминания.')
            return

        # Dыполняется вызов функции dbcreate.create_task, которая создает задачу в базе данных с указанием ID
        await dbcreate.create_task(message.chat.id, diary_content, date_time)

        # Бот уведомляет пользователя о создании напоминания и очищает состояние
        await message.answer(
            f'Вы создали напоминание:\n'
            f'Напоминание: {diary_content}\n'
            f'Время: {time_input}\n'
        )
        await state.clear()

    except ValueError:
        await message.answer('Неверный формат времени. Пожалуйста, введите дату и время в формате: "YYYY-MM-DD HH:MM".\n'
                             'Например: 2013-10-14 10:00')
    except Exception as e:
        await message.answer(f'Произошла ошибка: {str(e)}')