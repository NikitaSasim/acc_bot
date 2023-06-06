import openai
import logging

import requests
from aiogram.types import Message, CallbackQuery

import config

import json


def gpt(callback: CallbackQuery):

    openai.api_key = config.OPENAI_TOKEN
    print(openai.api_key)
    model_engine = "gpt-3.5-turbo"
    data = str(get_user(callback))
    print(data)
    prompt = f'look at this json, analyze my income and expenses and give your recommendations: {data}'
    print(prompt)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    print(response)

    return(response.choices[0].text)





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


    response = requests.post(url, data=data)


    return response.status_code

