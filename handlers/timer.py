from datetime import datetime, timedelta
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.states import Formtime
from keyboards import reply
from extensions import dbcreate


# Используется для организации маршрутов в боте.
router = Router()


now = datetime.now()
now_clean = datetime.now().strftime('%Y-%m-%d %H:%M')

next_day_one = now + timedelta(days=1)
next_day = next_day_one.strftime('%Y-%m-%d %H:%M')


# Этот обработчик активируется, когда пользователь отправляет сообщение с текстом 'создать задачу' или 'запланировать отдых'
@router.message(F.text.lower().in_(['новое напоминание', 'запланировать отдых']))
async def process_message(message: Message, state: FSMContext):
    # Состояние FSM устанавливается в Formtime.note, что указывает на ожидание ввода напоминания
    await state.set_state(Formtime.note)
    await message.answer('Введите текст напоминания:')


# Этот обработчик активируется, когда пользователь вводит текст
@router.message(Formtime.note)
async def form_class(message: Message, state: FSMContext):
    # Текст напоминания сохраняется в состоянии FSM
    await state.update_data(note=message.text)
    # Бот переводит состояние в Formtime.time, ожидая ввод даты и времени
    await state.set_state(Formtime.time)
    await message.answer(f'Введите дату и время в формате: "YYYY-MM-DD HH:MM".\n'
                         f'Например: {now_clean}')


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
            await message.answer(f'Время не может быть в прошлом. Пожалуйста, введите дату и время в будущем.\n'
                                 f'Например: {next_day}')
            return

        # Извлекается текст напоминания из состояния FSM, и если оно пустое, появляется соответствующее сообщение
        data = await state.get_data()
        diary_content = data.get('note')

        if not diary_content or diary_content.strip() == "":
            await message.answer('Содержимое напоминания не может быть пустым. Пожалуйста, введите текст напоминания.')
            return

        # Выполняется вызов функции dbcreate.create_task, которая создает задачу в базе данных с указанием ID
        await dbcreate.create_task(message.chat.id, diary_content, date_time)

        # Бот уведомляет пользователя о создании напоминания и очищает состояние
        await message.answer(
            f'Вы создали напоминание:\n'
            f'Напоминание: {diary_content}\n'
            f'Время: {time_input}\n',
            reply_markup=reply.tasks_kb
        )
        await state.clear()

    except ValueError:
        await message.answer(f'Неверный формат времени. Пожалуйста, введите дату и время в формате: "YYYY-MM-DD HH:MM".\n'
                             f'Например: {now_clean}')
    except Exception as e:
        await message.answer(f'Произошла ошибка: {str(e)}')


@router.message(F.text.lower().in_(['список напоминаний']))
async def handle_get_user_task(message: Message):
    user_chat_id = message.from_user.id
    task = await dbcreate.get_user_task(user_chat_id)

    if task:
        tasks_list = '\n'.join([
            f'ID напоминания: {t.id}\nНапоминание: {t.inner_text}\nДата и время: {t.timer}\n'
            for t in task
        ])
        await message.answer(f'Ваши напоминания:\n\n{tasks_list}', reply_markup=reply.list_tasks_kb)
    else:
        await message.answer('У вас нет напоминаний.')


@router.message(F.text.lower().in_(['удалить напоминание']))
async def handle_delete_tasks(message: Message, state: FSMContext):
    # Здесь мы получаем уникальный идентификатор пользователя, отправившего сообщение
    user_chat_id = message.from_user.id
    task = await dbcreate.get_user_task(user_chat_id)

    if task:
        tasks_list = '\n'.join([
            f'ID напоминания: {t.id}\nНапоминание: {t.inner_text}\nДата и время: {t.timer}\n'
            for t in task
        ])
        await message.answer(f'Ваши напоминания:\n{tasks_list}\n'
                             'Введите ID напоминания:')

        # Сохраняем состояние, чтобы позже знать, что пользователю нужно ввести ID заметки
        await state.update_data(user_request='task_id')
    else:
        await message.answer('У вас нет напоминаний.')

    @router.message(lambda message: message.text.isdigit())
    async def confirm_delete_note(message: Message, state: FSMContext):
        # Получаем chat_id пользователя
        user_chat_id = message.from_user.id
        # Получаем заголовок заметки для удаления
        task_id = int(message.text)

        # Получаем данные состояния
        data = await state.get_data()

        # Мы проверяем, действительно ли предыдущим шагом было запросить ID заметки
        if data.get('user_request') == 'task_id':
            # Пытаемся удалить заметку
            try:
                result = await dbcreate.delete_task(user_chat_id=user_chat_id, task_id=task_id)

                if result:
                    await message.answer(f'Напоминание "{task_id}" было удалено.', reply_markup=reply.list_tasks_kb)
                else:
                    await message.answer(f'Напоминание "{task_id}" не найдено. Пожалуйста, проверьте ID.')
            except Exception as e:
                await message.answer(f'Ошибка при удалении напоминания: {str(e)}')

        # Завершаем текущее состояние, чтобы сбросить контекст.
        await state.clear()


@router.message(F.text.lower().in_(['редактировать напоминание']))
async def handle_edit_tasks(message: Message, state: FSMContext):
    # Здесь мы получаем уникальный идентификатор пользователя, отправившего сообщение
    user_chat_id = message.from_user.id
    task = await dbcreate.get_user_task(user_chat_id)

    if task:
        tasks_list = '\n'.join([
            f'ID напоминания: {t.id}\nНапоминание: {t.inner_text}\nДата и время: {t.timer}\n'
            for t in task
        ])
        await message.answer(f'Ваши напоминания:\n{tasks_list}\n'
                             'Введите ID напоминания:')

        # Сохраняем состояние, чтобы позже знать, что пользователю нужно ввести ID заметки
        await state.set_state('waiting_for_task_id')
    else:
        await message.answer('У вас нет напоминаний.')

    @router.message(StateFilter('waiting_for_task_id'))
    async def input_task_id(message: Message, state: FSMContext):
        task_id = message.text.strip()

        if task_id.isdigit():
            task_id = int(task_id)
            await state.update_data(task_id=task_id)
            await message.answer('Введите новое напоминание:')
            await state.set_state('waiting_for_new_body')
        else:
            await message.answer('Пожалуйста, введите корректный ID напоминания.')

    @router.message(StateFilter('waiting_for_new_body'))
    async def update_task_body(message: Message, state: FSMContext):
        new_body = message.text
        await state.update_data(new_body=new_body)
        await message.answer(f'Введите новую дату и время в формате: "YYYY-MM-DD HH:MM".\n'
                             f'Например: {now_clean}')
        await state.set_state('waiting_for_new_time')

    @router.message(StateFilter('waiting_for_new_time'))
    async def update_note_time(message: Message, state: FSMContext):
        new_time_str = message.text
        data = await state.get_data()
        user_chat_id = message.from_user.id
        task_id = data.get('task_id')
        new_inner_text = data.get('new_body')

        try:
            new_timer_str = datetime.strptime(new_time_str, "%Y-%m-%d %H:%M")

            if new_timer_str <= datetime.now():
                await message.answer(f'Время не может быть в прошлом. Пожалуйста, введите дату и время в будущем.\n'
                                     f'Например: {next_day}')
                return

        except ValueError:
            await message.answer(f'Неверный формат времени. Пожалуйста, введите дату и время в формате: "YYYY-MM-DD HH:MM".\n'
                                 f'Например: {now_clean}')
            return

        if task_id is not None:
            try:
                result = await dbcreate.edit_task(
                    user_chat_id=user_chat_id,
                    task_id=task_id,
                    new_inner_text=new_inner_text,
                    new_timer_str=new_timer_str
                )

                if result:
                    await message.answer(f'Напоминание "{task_id}" было отредактировано.', reply_markup=reply.list_tasks_kb)
                else:
                    await message.answer(f'Напоминание "{task_id}" не найдено. Пожалуйста, проверьте ID.')
            except Exception as e:
                await message.answer(f'Ошибка при редактировании напоминания: {str(e)}')
        else:
            await message.answer('ID Напоминания не найден. Пожалуйста, попробуйте снова.')

        await state.clear()
