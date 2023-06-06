from aiogram import F, Router, types, flags
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from datetime import datetime
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

import utils
from states import IncomeForm, ExpenseForm

import kb
import text

router = Router()

"""
Common menus and functions
"""
@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
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
    # rec = utils.gpt(callback)

    await callback.message.answer(text=utils.gpt(callback), reply_markup=kb.menu)

"""
Income filling
"""

@router.callback_query(F.data == "income")
async def add_income(callback: CallbackQuery, state: FSMContext):

    await state.set_state(IncomeForm.income_category)

    keyboard = []
    keys = []
    IncomeForm.categories = utils.incomes_categories(callback)[1]
    IncomeForm.categories_dict = utils.incomes_categories(callback)[0]
    for i in range(len(IncomeForm.categories)):
        key = KeyboardButton(text=IncomeForm.categories[i])
        keys.append(key)
        if i % 2 != 0:
            keyboard.append(keys)
            keys = []

    keyboard.append([kb.exit_key, ])
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, selective=True, )


    await callback.message.answer("What is your category?", reply_markup=markup)


@router.message(lambda message: message.text not in IncomeForm.categories, IncomeForm.income_category)
async def process_income_category_invalid(message: types.Message):

    return await message.reply(f"Bad category name. Choose category from the keyboard.")


@router.message(IncomeForm.income_category)
async def process_income_category(message: types.Message, state=FSMContext):
    IncomeForm.category = message.text
    await state.update_data(income_category=message.text)
    await state.set_state(IncomeForm.income_date)
    await message.answer(
        "Input income date \n in format: DD.MM.YYY",
        reply_markup=kb.exit_kb,
    )

@router.message(IncomeForm.income_date)
async def process_income_date(message: types.Message, state=FSMContext):
    try:
        date = datetime.strptime(message.text, '%d.%m.%Y')
        date = datetime.date(date)
        print(date)
        await state.update_data(income_date=date)
        await state.set_state(IncomeForm.income_amount)
        await message.answer(
            "Input income amount",
            reply_markup=kb.exit_kb,
        )
    except:
        await message.answer(
            "Input correct income date \n in format: DD.MM.YYY",
            reply_markup=kb.exit_kb,
        )

@router.message(IncomeForm.income_amount)
async def process_income_amount(message: types.Message, state=FSMContext):
    try:
        await state.update_data(income_amount=float(message.text))


    except:
        return await message.answer(
            "Input correct amount",
            reply_markup=kb.exit_kb,
        )
    await state.set_state(IncomeForm.income_narration)
    await message.answer(
        "Input income narration",
        reply_markup=kb.exit_kb,)

@router.message(IncomeForm.income_narration)
async def process_income_narration(message: types.Message, state=FSMContext):

    try:
        await state.update_data(income_narration=message.text)

    except:
        await message.answer(
            "Input correct narration",
            reply_markup=kb.exit_kb,
        )
    await state.set_state(IncomeForm.income_is_ready)
    # await message.answer(text.income_confirmation.format(category=IncomeForm.category, date=IncomeForm.income_date),
    #                      reply_markup=kb.income_confirmation_kb)
    data = await state.get_data()

    await message.answer(text.income_confirmation.format(
        category=data['income_category'],
        date=data['income_date'].strftime("%d.%m.%Y"),
        ammount=data['income_amount'],
        narration=data['income_narration']
    ), reply_markup=kb.income_confirmation_kb)

@router.callback_query(F.data == "post_income")
async def add_income(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.update_data(income_category=IncomeForm.categories_dict[data['income_category']])
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











#
# @router.message(Gen.text_prompt)
# @flags.chat_action("typing")
# async def generate_text(msg: Message, state: FSMContext):
#     prompt = msg.text
#     mesg = await msg.answer(text.gen_wait)
#     res = await utils.generate_text(prompt)
#     if not res:
#         return await mesg.edit_text(text.gen_error, reply_markup=kb.iexit_kb)
#     await mesg.edit_text(res[0] + text.text_watermark, disable_web_page_preview=True)
#
# @router.callback_query(F.data == "generate_image")
# async def input_image_prompt(clbck: CallbackQuery, state: FSMContext):
#     await state.set_state(Gen.img_prompt)
#     await clbck.message.edit_text(text.gen_image)
#     await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)
#
# @router.message(Gen.img_prompt)
# @flags.chat_action("upload_photo")
# async def generate_image(msg: Message, state: FSMContext):
#     prompt = msg.text
#     mesg = await msg.answer(text.gen_wait)
#     img_res = await utils.generate_image(prompt)
#     if len(img_res) == 0:
#         return await mesg.edit_text(text.gen_error, reply_markup=kb.iexit_kb)
#     await mesg.delete()
#     await mesg.answer_photo(photo=img_res[0], caption=text.img_watermark)