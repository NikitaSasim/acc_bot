import openai
import logging

import requests
from aiogram.types import Message, CallbackQuery

import config

openai.api_key = config.OPENAI_TOKEN
import json


async def generate_text(prompt) -> dict:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'], response['usage']['total_tokens']
    except Exception as e:
        logging.error(e)


async def generate_image(prompt, n=1, size="1024x1024") -> list[str]:
    try:
        response = await openai.Image.acreate(
            prompt=prompt,
            n=n,
            size=size
        )
        urls = []
        for i in response['data']:
            urls.append(i['url'])
    except Exception as e:
        logging.error(e)
        return []
    else:
        return urls


def incomes_categories(callback: CallbackQuery):
    user_id = callback.from_user.id
    print(user_id)
    url = "http://127.0.0.1:8000/api/incomes_categories/"
    params = {
        'user': user_id,
    }
    response = requests.get(url, params)

    categories = {item['name']: item['id'] for item in response.json()}
    categories_names = tuple(categories)


    return categories, categories_names

def get_user(callback: CallbackQuery):
    user_id = callback.from_user.id
    print(user_id)
    url = "http://127.0.0.1:8000/api/user/"
    acc_token = config.ACC_TOKEN
    print(acc_token)
    params = {
        'user': user_id,
        'token': acc_token
    }
    response = requests.get(url, params)
    print(response.json())

    return response.json()

def post_income(data):
    url = "http://127.0.0.1:8000/api/post_income/"
    # acc_token = config.ACC_TOKEN
    # params = data
    # # params["token"] = acc_token
    # data = json.dumps(params)
    print(data)
    response = requests.post(url, data=data)

    print(response.status_code)
    return response.status_code

