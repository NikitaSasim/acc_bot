from aiogram.fsm.state import StatesGroup, State


class IncomeForm(StatesGroup):
    income_category = State()
    income_date = State()
    income_amount = State()
    income_narration = State()
    income_is_ready = State()
    categories = list
    categories_dict = dict



class ExpenseForm(StatesGroup):
    expense_category = State()
    expense_date = State()
    expense_amount = State()
    expense_narration = State()


