import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
ACC_TOKEN = os.getenv("ACC_TOKEN")
URL = os.getenv("URL")
