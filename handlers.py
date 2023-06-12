from aiogram import F, Router, types, flags
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from datetime import datetime

from aiogram.fsm.context import FSMContext



import utils
from states import Form, Form

import kb
import text

router = Router()

"""
Common menus and functions
"""

@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    if len(message.text.split()) > 1:
        await utils.set_id(message)

    await state.clear()
    await message.answer(text='💵💵💵💵💵💵💵💵💵💵💵💵💵💵💵', reply_markup=ReplyKeyboardRemove())
    await message.answer(text.greet.format(name=message.from_user.full_name), reply_markup=kb.menu)


@router.message(F.text == "Exit")
@router.message(F.text == "Menu")
@router.message(F.text == "◀️ Exit to main menu")
async def menu(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(text='💵💵💵💵💵💵💵💵💵💵💵💵💵💵💵', reply_markup=ReplyKeyboardRemove())
    await message.answer(text.menu, reply_markup=kb.menu)


@router.callback_query(F.data == "menu")
async def menu_no(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(text='💵💵💵💵💵💵💵💵💵💵💵💵💵💵💵', reply_markup=ReplyKeyboardRemove())
    await callback.message.answer(text.menu, reply_markup=kb.menu)



@router.callback_query(F.data == "recommendations")
async def recommendations(callback: CallbackQuery):
    await callback.message.answer(text=utils.gpt(callback), reply_markup=kb.menu)


"""
Income filling
"""


@router.callback_query(F.data == "income")
async def add_income(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Form.income_category)
    router.parent_router
    keyboard = []
    keys = []
    Form.income_categories = utils.incomes_categories(callback)[1]
    Form.income_categories_dict = utils.incomes_categories(callback)[0]
    for i in range(len(Form.income_categories)):
        key = KeyboardButton(text=Form.income_categories[i])
        keys.append(key)
        if i % 2 != 0:
            keyboard.append(keys)
            keys = []
    if keys == []:
        keyboard.append([kb.exit_key, ])
    else:
        keys.append(kb.exit_key)
        keyboard.append(keys)
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, selective=True, )


    await callback.message.answer(text.category, reply_markup=markup)


@router.message(lambda message: message.text not in Form.income_categories, Form.income_category)
async def process_income_category_invalid(message: types.Message):

    return await message.reply("Bad category name. Choose category from the keyboard.")


@router.message(Form.income_category)
async def process_income_category(message: types.Message, state=FSMContext):
    Form.category = message.text
    await state.update_data(income_category=message.text)

    await state.set_state(Form.income_date)
    await message.answer(
        "Input income date \n in format: DD.MM.YYY",
        reply_markup=kb.exit_kb,
    )


@router.message(Form.income_date)
async def process_income_date(message: types.Message, state=FSMContext):
    try:
        date = datetime.strptime(message.text, '%d.%m.%Y')
        date = datetime.date(date)

        await state.update_data(income_date=date)
        await state.set_state(Form.income_amount)
        await message.answer(
            "Input income amount",
            reply_markup=kb.exit_kb,
        )
    except:
        await message.answer(
            "Input correct income date \n in format: DD.MM.YYY",
            reply_markup=kb.exit_kb,
        )


@router.message(Form.income_amount)
async def process_income_amount(message: types.Message, state=FSMContext):
    try:
        await state.update_data(income_amount=float(message.text))


    except:
        return await message.answer(
            "Input correct amount",
            reply_markup=kb.exit_kb,
        )
    await state.set_state(Form.income_narration)
    await message.answer(
        "Input income narration",
        reply_markup=kb.exit_kb,)


@router.message(Form.income_narration)
async def process_income_narration(message: types.Message, state=FSMContext):

    try:
        await state.update_data(income_narration=message.text)

    except:
        await message.answer(
            "Input correct narration",
            reply_markup=kb.exit_kb,
        )
    await state.set_state(Form.income_is_ready)
    # await message.answer(text.income_confirmation.format(category=Form.category, date=Form.income_date),
    #                      reply_markup=kb.income_confirmation_kb)
    data = await state.get_data()

    await message.answer(text.confirmation.format(
        category=data['income_category'],
        date=data['income_date'].strftime("%d.%m.%Y"),
        ammount=data['income_amount'],
        narration=data['income_narration']
    ), reply_markup=kb.income_confirmation_kb)


@router.callback_query(F.data == "post_income", Form.income_is_ready)
async def add_income(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.update_data(income_category=Form.income_categories_dict[data['income_category']])
    data = await state.get_data()

    params = {
        "user": utils.get_user(callback)["user"],
        "category": data["income_category"],
        "date": data["income_date"].strftime("%Y.%m.%d"),
        "amount": data["income_amount"],
        "narration": data["income_narration"],
    }
    print(params)
    await callback.message.answer(utils.post_income(params), reply_markup=kb.exit_kb)

"""
Expenses filling
"""

@router.callback_query(F.data == "expense")
async def add_expense(callback: CallbackQuery, state: FSMContext):

    await state.set_state(Form.expense_category)

    keyboard = []
    keys = []
    Form.expense_categories = utils.expenses_categories(callback)[1]
    Form.expense_categories_dict = utils.expenses_categories(callback)[0]
    for i in range(len(Form.expense_categories)):
        key = KeyboardButton(text=Form.expense_categories[i])
        keys.append(key)
        if i % 2 != 0:
            keyboard.append(keys)
            keys = []
    if keys == []:
        keyboard.append([kb.exit_key, ])
    else:
        keys.append(kb.exit_key)
        keyboard.append(keys)
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, selective=True, )


    await callback.message.answer(text.category, reply_markup=markup)


@router.message(lambda message: message.text not in Form.expense_categories, Form.expense_category)
async def process_expense_category_invalid(message: types.Message):

    return await message.reply("Bad category name. Choose category from the keyboard.")


@router.message(Form.expense_category)
async def process_expense_category(message: types.Message, state=FSMContext):
    # Form.category = message.text
    await state.update_data(expense_category=message.text)

    await state.set_state(Form.expense_date)
    await message.answer(
        "Input expense date \n in format: DD.MM.YYY",
        reply_markup=kb.exit_kb,
    )


@router.message(Form.expense_date)
async def process_expense_date(message: types.Message, state=FSMContext):
    try:
        date = datetime.strptime(message.text, '%d.%m.%Y')
        date = datetime.date(date)

        await state.update_data(expense_date=date)
        await state.set_state(Form.expense_amount)
        await message.answer(
            "Input expense amount",
            reply_markup=kb.exit_kb,
        )
    except:
        await message.answer(
            "Input correct expense date \n in format: DD.MM.YYY",
            reply_markup=kb.exit_kb,
        )


@router.message(Form.expense_amount)
async def process_expense_amount(message: types.Message, state=FSMContext):
    try:
        await state.update_data(expense_amount=float(message.text))


    except:
        return await message.answer(
            "Input correct amount",
            reply_markup=kb.exit_kb,
        )
    await state.set_state(Form.expense_narration)
    await message.answer(
        "Input expense narration",
        reply_markup=kb.exit_kb,)


@router.message(Form.expense_narration)
async def process_expense_narration(message: types.Message, state=FSMContext):

    try:
        await state.update_data(expense_narration=message.text)

    except:
        await message.answer(
            "Input correct narration",
            reply_markup=kb.exit_kb,
        )
    await state.set_state(Form.expense_is_ready)
    # await message.answer(text.expense_confirmation.format(category=Form.category, date=Form.expense_date),
    #                      reply_markup=kb.expense_confirmation_kb)
    data = await state.get_data()

    await message.answer(text.confirmation.format(
        category=data['expense_category'],
        date=data['expense_date'].strftime("%d.%m.%Y"),
        ammount=data['expense_amount'],
        narration=data['expense_narration']
    ), reply_markup=kb.expense_confirmation_kb)


@router.callback_query(F.data == "post_expense", Form.expense_is_ready)
async def add_expense(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.update_data(expense_category=Form.expense_categories_dict[data['expense_category']])
    data = await state.get_data()

    params = {
        "user": utils.get_user(callback)["user"],
        "category": data["expense_category"],
        "date": data["expense_date"].strftime("%Y.%m.%d"),
        "amount": data["expense_amount"],
        "narration": data["expense_narration"],
    }
    print(params)
    await callback.message.answer(utils.post_expense(params), reply_markup=kb.exit_kb)

