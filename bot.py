import asyncio

from aiogram import Bot, Dispatcher, executor, types
import config
# import messages
# import keyboard
# from coordinates import Coordinates
from api import incomes_categories
import begetter


bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)

Users = dict()

#
# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     await message.answer(text=f"Привет, {message.from_user.first_name}!\n"
#                               f"О чем ты хочешь поговорить?")
#
#
# @dp.message_handler()
# async def conversation(message: types.Message):
#     await message.answer(text=gpt(message))




@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(text=f"Hellow, {message.from_user.first_name}!\n"
                              f"To add an income entry press\n"
                              f"\n"
                              f""
                              f"/income\n"
                              f"\n"
                              f"To add an expense entry press\n"
                              f"\n"
                              f""
                              f"/expense\n")

@dp.message_handler(commands=['income'])
async def income(message):
    await asyncio.create_task(message.answer(begetter.income(incomes_categories(message))))
    # task = begetter.make_funk(incomes_categories(message))
    # task = asyncio.create_task(message.answer(begetter.make_funk(incomes_categories(message))))
    # exec(task)
    # await asyncio.create_subprocess_exec(begetter.make_funk(incomes_categories(message)))
    # async def task = exec(begetter.make_funk(incomes_categories(message)))



    # # await message.answer(text=incomes_categories(message))
    # # task2 = asyncio.create_subprocess_exec()
    #
    await task
    pass





async def main(message):
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Started")
    executor.start_polling(dp)
