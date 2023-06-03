# import os
# import openai
# import config
from aiogram import types
import requests


# openai.api_key = os.getenv(config.OPENAI_API_KEY)

# openai.Model.list()

# url = "https://api.openai.com/v1/models"
# headers = {"Authorization": "Bearer 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"}
# response = requests.get(url, headers=headers)
# print(response)
# print(response.json())


# def gpt(message: types.Message):
#
#     openai.api_key = config.OPENAI_API_KEY
#     model_engine = "text-davinci-003"
#
#     completion = openai.Completion.create(
#         engine=model_engine,
#         prompt=message.text,
#         max_tokens=1024,
#         temperature=0.5,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=-1
#     )
#     with open(f'log\{message.from_user.id}.txt', 'a', newline='\n') as log:
#         log.writelines(f'{message.from_user.username}   {message.date}   {message.text}'+'\n')
#         log.writelines(f'Bot: {completion.choices[0].text}'+'\n')
#
#     return(completion.choices[0].text)

# def gpt(message: types.Message):
#
#     openai.api_key = config.OPENAI_API_KEY
#     model_engine = "gpt-3.5-turbo"
#
#     completion = openai.ChatCompletion.create(
#         engine=model_engine,
#         prompt=message.text,
#         max_tokens=1024,
#         temperature=0.5,
#         frequency_penalty=0,
#         presence_penalty=-1
#     )
#     with open(f'log\{message.from_user.id}.txt', 'a', newline='\n') as log:
#         log.writelines(f'{message.from_user.username}   {message.date}   {message.text}'+'\n')
#         log.writelines(f'Bot: {completion.choices[0].text}'+'\n')
#
#     return(completion.choices[0].text)

def incomes_categories(message: types.Message):
    print(message.from_user.id)
    url = "http://127.0.0.1:8000/api/incomes_categories/"
    params = {
        'user': 1,
    }
    response = requests.get(url, params)



    return response.json()
