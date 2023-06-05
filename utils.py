import openai
import logging

import requests
from aiogram.types import Message, CallbackQuery

import config

openai.api_key = config.OPENAI_TOKEN


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

def post_income(data):
    url = "http://127.0.0.1:8000/api/post_income/"
    response = requests.post(url, params=data)
    print(response.status_code)
    return response.status_code

