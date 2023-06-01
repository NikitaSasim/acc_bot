from aiogram import Bot, Dispatcher, executor, types
import config
# import messages
# import keyboard
# from coordinates import Coordinates
from gpt import gpt


bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)

Users = dict()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(text=f"Привет, {message.from_user.first_name}!\n"
                              f"О чем ты хочешь поговорить?")


@dp.message_handler()
async def conversation(message: types.Message):
    await message.answer(text=gpt(message))








async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Started")
    executor.start_polling(dp)
