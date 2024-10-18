from aiogram.fsm.state import StatesGroup, State


# Создание всех полей ввода для dairy и timer
class Form(StatesGroup):
    name_dairy = State()
    text_dairy = State()


class Formtime(StatesGroup):
    note = State()
    time = State()

