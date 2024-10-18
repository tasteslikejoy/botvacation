from contextlib import suppress
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from keyboards import fabrics
from data.subloader import get_json


router = Router()


# Этот декоратор используется для настройки обработчика callback-запросов Telegram
# Он фильтрует только те события, которые соответствуют заданному условию – в данном случае, когда значение action (prev или next) в callback-данных
@router.callback_query(fabrics.Pag.filter(F.action.in_(['prev_bags', 'next_bags'])))
# Функция обрабатывает нажатия на кнопки навигации, которые находятся в сообщении бота
# call: объект CallbackQuery, который содержит информацию о запросе
# callback_data: данные, отправленные вместе с запросом, которые здесь фильтруются с помощью fabrics.Pag
async def pagination(call: CallbackQuery, callback_data: fabrics.Pag):
    # Загрузка данных из файла bags.json с помощью асинхронной функции get_json
    # Файл содержит массив с данными
    bags = await get_json('bags.json')
    # Переменная page_num получает номер текущей страницы из callback_data, который конвертируется в целое число
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    if callback_data.action == 'next_bags':
        page = page_num + 1 if page_num < (len(bags) - 1) else page_num
    # Используется контекстный менеджер with suppress(TelegramBadRequest), который подавляет возможные исключения TelegramBadRequest
    # Тестовый случай, использован 1 раз в коде (далее везде try/except)
    with suppress(TelegramBadRequest):
        # Функция edit_text редактирует текст сообщения, заменяя его на данные из актуального элемента массива bags
        # и прикрепляет обновленную клавиатуру с помощью функции fabrics.pag(page)
        # которая также формирует новую клавиатуру в зависимости от текущей страницы
        await call.message.edit_text(
            f'{bags[page][0]} {bags[page][1]}',
            reply_markup=fabrics.pag_bags(page)
        )
    # await call.answer() отправляет ответ на callback-запрос
    await call.answer()

@router.callback_query(fabrics.Pag.filter(F.action.in_(['prev_cloth', 'next_cloth'])))
async def pagination_cloth(call: CallbackQuery, callback_data: fabrics.Pag):
    cloth = await get_json('cloth.json')

    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    if callback_data.action == 'next_cloth':
        page = page_num + 1 if page_num < (len(cloth) - 1) else page_num

    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f'{cloth[page][0]} {cloth[page][1]}',
            reply_markup=fabrics.pag_cloth(page)
        )
    await call.answer()

@router.callback_query(fabrics.Pag.filter(F.action.in_(['prev_cosm', 'next_cosm'])))
async def pagination_cosm(call: CallbackQuery, callback_data: fabrics.Pag):
    cosmetics = await get_json('cosmetics.json')

    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    if callback_data.action == 'next_cosm':
        page = page_num + 1 if page_num < (len(cosmetics) - 1) else page_num

    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f'{cosmetics[page][0]} {cosmetics[page][1]}',
            reply_markup=fabrics.pag_cosmetics(page)
        )
    await call.answer()

@router.callback_query(fabrics.Pag.filter(F.action.in_(['prev_el', 'next_el'])))
async def pagination_el(call: CallbackQuery, callback_data: fabrics.Pag):
    electronic_equipment = await get_json('electronic_equipment.json')

    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    if callback_data.action == 'next_el':
        page = page_num + 1 if page_num < (len(electronic_equipment) - 1) else page_num

    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f'{electronic_equipment[page][0]} {electronic_equipment[page][1]}',
            reply_markup=fabrics.pag_electronic(page)
        )
    await call.answer()

@router.callback_query(fabrics.Pag.filter(F.action.in_(['prev_med', 'next_med'])))
async def pagination_med(call: CallbackQuery, callback_data: fabrics.Pag):
    medicines = await get_json('medicines.json')

    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    if callback_data.action == 'next_med':
        page = page_num + 1 if page_num < (len(medicines) - 1) else page_num

    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f'{medicines[page][0]} {medicines[page][1]}',
            reply_markup=fabrics.pag_medicine(page)
        )
    await call.answer()