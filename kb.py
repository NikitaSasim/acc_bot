from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

menu = [
    [InlineKeyboardButton(text="💰 Add income", callback_data="income"),
    InlineKeyboardButton(text="💳 Add expense", callback_data="expense")],
    [InlineKeyboardButton(text="🧠 Get recommendations", callback_data="recommendations")]
]


menu = InlineKeyboardMarkup(inline_keyboard=menu, )
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Exit to main menu")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Exit to main menu", callback_data="menu")]])
exit_key = KeyboardButton(text="◀️ Exit to main menu")
income_confirmation_kb = InlineKeyboardMarkup(inline_keyboard=[
                                                            [InlineKeyboardButton(text="Yes", callback_data="post_income"),
                                                             InlineKeyboardButton(text="No", callback_data="menu")]
                                                            ])
