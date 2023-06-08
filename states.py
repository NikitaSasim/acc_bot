from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    income_category = State()
    income_date = State()
    income_amount = State()
    income_narration = State()
    income_is_ready = State()
    income_categories = list
    income_categories_dict = dict

    expense_category = State()
    expense_date = State()
    expense_amount = State()
    expense_narration = State()
    expense_is_ready = State()
    expense_categories = list
    expense_categories_dict = dict


