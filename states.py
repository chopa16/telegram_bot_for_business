from aiogram.dispatcher.filters.state import StatesGroup, State


class User_info(StatesGroup):
    Q1 = State()
class ChosenThing(StatesGroup):
    choose_size = State()
    choose_quantity = State()
