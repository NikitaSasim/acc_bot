

def income(categories):
    categories_list = ''

    for category in categories:
        name = category['name']
        name = name.replace(' ', '_')
        categories_list = categories_list + f"/{name}\n"


    return categories_list

def make_funk(categories):
    # scrypt = "import asyncio\n"
    # scrypt += "from aiogram import Bot, Dispatcher, executor, types\n"
    # scrypt += "import config\n"
    # scrypt += "from api import incomes_categories\n"
    # scrypt += "import begetter\n"
    # scrypt += "bot = Bot(token=config.BOT_API_TOKEN)\n"
    # scrypt += "dp2 = Dispatcher(bot)\n"
    # scrypt += "Users = dict()\n"

    scrypt = ""

    for category in categories:
        name = category['name']
        name = name.replace(' ', '_')

        scrypt += f"@dp.message_handler(commands=['[{name}]'])\n"
        scrypt += f"async def income(message: types.Message):\n"
        scrypt += f"    await message.answer(text='Input amount')\n\n"

    # scrypt += f"async def main(message):\n"
    # scrypt += f"    await dp.start_polling(bot)\n"
    # scrypt += f"if __name__ == '__main__':\n"
    # scrypt += f"    print('scrypt is running')\n"
    # scrypt += f"    executor.start_polling(dp)\n"
    #





    scrypt = compile(scrypt, 'test', "exec")

    return scrypt


# def making_dict
#
#
# scrypt = ''
# for name in ['name1', 'name2', 'name3']:
#     scrypt += f'def {name}():\n    {name} = "{name}"\n    print({name})\n'
#
# for name in ['name1', 'name2', 'name3']:
#     scrypt += f'{name}()\n'
#
# print(scrypt)
#
# f = compile(scrypt, 'test', "exec")
# exec(f)


