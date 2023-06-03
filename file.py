import asyncio

from aiogram import Bot, Dispatcher, executor, types
import config

from api import incomes_categories
import begetter


bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)

Users = dict()



async def main(message):
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Started")
    executor.start_polling(dp)
