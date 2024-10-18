from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.states import Form
from keyboards import reply
from extensions import dbcreate


# Используется для организации маршрутов в боте.
router = Router()


# Этот обработчик активируется, когда пользователь отправляет сообщение с текстом 'новая заметка'
@router.message(F.text.lower().in_(['новая заметка']))
async def add_dairy(message: Message, state: FSMContext):
    # Состояние устанавливается на Form.class_dairy, что означает, что бот теперь ожидает, что пользователь введет категорию для своей заметки
    await state.set_state(Form.name_dairy)
    await message.answer('Заголовок:', reply_markup=reply.call_dairy_kb)


# Здесь обрабатывается ввод заголовка
@router.message(Form.name_dairy)
async def form_name(message: Message, state: FSMContext):
    # Заголовок сохраняется (в name_dairy)
    await state.update_data(name_dairy=message.text)
    # Cостояние меняется на Form.text_dairy для получения текста заметки
    await state.set_state(Form.text_dairy)
    await message.answer('Текст:', reply_markup=reply.call_dairy_kb)


# Здесь бот ожидает текст самой заметки
@router.message(Form.text_dairy)
async def form_text(message: Message, state: FSMContext):
    # После ввода текста заметки, он сохраняется в состоянии (в text_dairy)
    await state.update_data(text_dairy=message.text)
    # С помощью await state.get_data() бот получает все данные, введенные пользователем
    data = await state.get_data()
    caption = data.get('name_dairy') # Извлекаем название заметки
    body = data['text_dairy']  # Получаем текст

    # Пытаемся создать заметку
    try:
        note_id = await dbcreate.add_note(
            user_chat_id=message.chat.id,
            caption=caption,
            body=body
        )
        await message.answer(f'Заметка создана: {note_id}', reply_markup=reply.list_dairy_kb)
    except Exception as e:
        await message.answer(f'Ошибка: {str(e)}')
    # Процесс завершается очисткой состояния с помощью await state.clear()
    await state.clear()


# Определяется асинхронная функция, принимающая параметр message, который содержит информацию о полученном сообщении от пользователя
@router.message(F.text.lower().in_(['список заметок']))
async def handle_get_user_notes(message: Message):
    # Из полученного сообщения извлекается идентификатор пользователя (chat_id), чтобы впоследствии использовать его для получения заметок из базы данных
    user_chat_id = message.from_user.id

    # Здесь вызывается асинхронная функция get_user_notes из модуля dbcreate, которая принимает user_chat_id и возвращает список заметок, связанных с этим пользователем
    notes = await dbcreate.get_user_notes(user_chat_id)

    if notes:
        notes_list = '\n'.join([
            f'ID заметки: {note.id}\nЗаголовок: {note.caption}\nЗаметка: {note.body}\n'
            for note in notes
        ])
        await message.answer(f'Ваши заметки:\n\n{notes_list}', reply_markup=reply.list_dairy_kb)
    else:
        await message.answer('У вас нет заметок.')


# Этот декоратор определяет, что функция будет вызвана при получении сообщения, содержащего текст 'удалить заметку'
@router.message(F.text.lower().in_(['удалить заметку']))
async def handle_delete_note(message: Message, state: FSMContext):
    # Здесь мы получаем уникальный идентификатор пользователя, отправившего сообщение
    user_chat_id = message.from_user.id

    # Функция запрашивает базу данных для получения всех заметок, связанных с пользователем
    notes = await dbcreate.get_user_notes(user_chat_id)

    if notes:
        # Формируем и отправляем сообщение с перечислением всех заметок и запрашиваем ввод ID заметки для удаления
        notes_list = '\n'.join([
            f'ID заметки: {note.id}\nЗаголовок: {note.caption}\nЗаметка: {note.body}\n'
            for note in notes
        ])
        await message.answer(f'Ваши заметки:\n{notes_list}\n'
                             'Введите ID заметки:')

        # Сохраняем состояние, чтобы позже знать, что пользователю нужно ввести ID заметки
        await state.update_data(user_request='note_id')
    else:
        await message.answer('У вас нет заметок.')

    # Этот обработчик запускается при получении сообщения, содержащего только цифры
    @router.message(lambda message: message.text.isdigit())
    async def confirm_delete_note(message: Message, state: FSMContext):
        # Получаем chat_id пользователя
        user_chat_id = message.from_user.id
        # Получаем заголовок заметки для удаления
        note_id = int(message.text)

        # Получаем данные состояния
        data = await state.get_data()

        # Мы проверяем, действительно ли предыдущим шагом было запросить ID заметки
        if data.get('user_request') == 'note_id':
            # Пытаемся удалить заметку
            try:
                result = await dbcreate.delete_note(user_chat_id=user_chat_id, note_id=note_id)

                if result:
                    await message.answer(f'Заметка "{note_id}" была удалена.', reply_markup=reply.list_dairy_kb)
                else:
                    await message.answer(f'Заметка "{note_id}" не найдена. Пожалуйста, проверьте ID.')
            except Exception as e:
                await message.answer(f'Ошибка при удалении заметки: {str(e)}')

        # Завершаем текущее состояние, чтобы сбросить контекст.
        await state.clear()


# Этот декоратор устанавливает обработчик для сообщений, содержащих текст 'редактировать заметку'
@router.message(F.text.lower().in_(['редактировать заметку']))
async def handle_edit_note(message: Message, state: FSMContext):
    # Получаем chat_id пользователя
    user_chat_id = message.from_user.id

    # Получаем все заметки
    notes = await dbcreate.get_user_notes(user_chat_id)

    if notes:
        # Формируем список заголовков заметок
        notes_list = '\n'.join([
            f'ID заметки: {note.id}\nЗаголовок: {note.caption}\nЗаметка: {note.body}\n'
            for note in notes
        ])
        await message.answer(f'Ваши заметки:\n{notes_list}\n'
                             'Введите ID заметки:')
        await state.set_state('waiting_for_note_id')
    else:
        await message.answer('У вас нет заметок.')

    # Этот обработчик срабатывает, когда бот находится в состоянии waiting_for_note_id
    # Если пользователь вводит корректный ID (число), бот обновляет состояние и просит ввести новый заголовок заметки
    # В противном случае он сообщает о неверном вводе
    @router.message(StateFilter('waiting_for_note_id'))
    async def input_note_id(message: Message, state: FSMContext):
        note_id = message.text.strip()

        if note_id.isdigit():
            note_id = int(note_id)
            await state.update_data(note_id=note_id)
            await message.answer('Введите новый заголовок для заметки:')
            await state.set_state('waiting_for_new_caption')
        else:
            await message.answer('Пожалуйста, введите корректный ID заметки.')

    # Когда пользователь находится в состоянии waiting_for_new_caption, бот принимает новый заголовок и запрашивает новое содержание заметки, меняя состояние на waiting_for_new_body.
    @router.message(StateFilter('waiting_for_new_caption'))
    async def update_note_caption(message: Message, state: FSMContext):
        new_caption = message.text
        await state.update_data(new_caption=new_caption)
        await message.answer('Введите новое содержание заметки:')
        await state.set_state('waiting_for_new_body')

    # Здесь обрабатывается ввод нового содержания заметки
    # Бот получает данные из состояния, включая ID заметки и новый заголовок, и пытается отредактировать заметку, вызывая функцию edit_note
    # Если операция успешна, бот уведомляет пользователя, что заметка была отредактирована
    # Если возникает какая-либо ошибка, отображается сообщение об ошибке.
    @router.message(StateFilter('waiting_for_new_body'))
    async def update_note_body(message: Message, state: FSMContext):
        new_body = message.text
        data = await state.get_data()
        user_chat_id = message.from_user.id
        note_id = data.get('note_id')
        new_caption = data.get('new_caption')

        if note_id is not None:
            try:
                result = await dbcreate.edit_note(
                    user_chat_id=user_chat_id,
                    note_id=note_id,
                    new_caption=new_caption,
                    new_body=new_body
                )

                if result:
                    await message.answer(f'Заметка "{note_id}" была отредактирована.', reply_markup=reply.list_dairy_kb)
                else:
                    await message.answer(f'Заметка "{note_id}" не найдена. Пожалуйста, проверьте ID.')
            except Exception as e:
                await message.answer(f'Ошибка при редактировании заметки: {str(e)}')
        else:
            await message.answer('ID заметки не найден. Пожалуйста, попробуйте снова.')

        await state.clear()

