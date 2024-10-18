from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


# Создание всех клавиатур в боте
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отпуск'),
            KeyboardButton(text='Ежедневник')
        ],
        [
            KeyboardButton(text='Интересный факт')
        ]
    ],
    resize_keyboard=True, # изменяет размер кнопок на маленькие
    input_field_placeholder='Я в своем познании настолько преисполнился...', # Текст отображается в поле ввода текста
)

dairy_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Список заметок')
        ],
        [
            KeyboardButton(text='Новая заметка')
        ],
        [
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True
)

list_dairy_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Удалить заметку')
        ],
        [
            KeyboardButton(text='Редактировать заметку')
        ],
        [
            KeyboardButton(text='Ежедневник')
        ]
    ],
    resize_keyboard=True
)

call_dairy_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ежедневник')
        ]
    ],
    resize_keyboard=True
)

vacation_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Предупредить начальство')
        ],
        [
            KeyboardButton(text='Начать отсчет')
        ],
        [
            KeyboardButton(text='Собрать вещи')
        ],
        [
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True
)

call_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отпуск')
        ]
    ],
    resize_keyboard=True
)

call_timer_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Создать задачу')
        ],
        [
            KeyboardButton(text='Отпуск')
        ]
    ],
    resize_keyboard=True
)

call_vacation_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Запланировать отдых')
        ],
        [
            KeyboardButton(text='Отпуск')
        ]
    ],
    resize_keyboard=True
)

bags_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Документы'),
            KeyboardButton(text='Одежда')
        ],
        [
            KeyboardButton(text='Лекарства'),
            KeyboardButton(text='Косметика')
        ],
        [
            KeyboardButton(text='Техника'),
            KeyboardButton(text='Отпуск')
        ],
    ],
    resize_keyboard=True
)