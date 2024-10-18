from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


# Здесь мы определяем класс Pag, который наследует от CallbackData
# Этот класс используется для упаковки и распаковки данных, которые будут передаваться через коллбек-кнопки в интерфейсе
class Pag(CallbackData, prefix='pag_bags'): # это префикс, который будет использоваться для коллбек-данных, чтобы их было легче идентифицировать при обработке
    action: str # переменная, которая будет хранить действие, например, "prev" (предыдущая страница) или "next" (следующая страница)
    page: int # переменная, которая будет хранить номер страницы


def pag_bags(page: int=0):
    builder_bags = InlineKeyboardBuilder() # создается экземпляр InlineKeyboardBuilder, который используется для построения инлайн-кнопок
    # Здесь мы добавляем ряд кнопок к клавиатуре. Метод row создает горизонтальный ряд кнопок
    builder_bags.row(
        InlineKeyboardButton(text='⬅', callback_data=Pag(action='prev_bags', page=page).pack()), # создается коллбек-данные для кнопки. Метод pack() упаковывает данные в строку, которую можно передать при нажатии на кнопку
        InlineKeyboardButton(text='➡', callback_data=Pag(action='next_bags', page=page).pack()),
        width=2 # количество кнопок в ряду
    )
    return builder_bags.as_markup() # В конце функция возвращает объект клавиатуры в виде разметки с помощью метода as_markup(), который подготавливает клавиатуру для отправки в сообщении

def pag_cloth(page: int=0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='⬅', callback_data=Pag(action='prev_cloth', page=page).pack()),
        InlineKeyboardButton(text='➡', callback_data=Pag(action='next_cloth', page=page).pack()),
        width=2
    )
    return builder.as_markup()

def pag_cosmetics(page: int=0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='⬅', callback_data=Pag(action='prev_cosm', page=page).pack()),
        InlineKeyboardButton(text='➡', callback_data=Pag(action='next_cosm', page=page).pack()),
        width=2
    )
    return builder.as_markup()

def pag_electronic(page: int=0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='⬅', callback_data=Pag(action='prev_el', page=page).pack()),
        InlineKeyboardButton(text='➡', callback_data=Pag(action='next_el', page=page).pack()),
        width=2
    )
    return builder.as_markup()

def pag_medicine(page: int=0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='⬅', callback_data=Pag(action='prev_med', page=page).pack()),
        InlineKeyboardButton(text='➡', callback_data=Pag(action='next_med', page=page).pack()),
        width=2
    )
    return builder.as_markup()