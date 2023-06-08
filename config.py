import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
OPENAI_TOKEN = os.environ.get('OPENAI_TOKEN')
ACC_TOKEN = os.environ.get('ACC_TOKEN')

# BOT_TOKEN = "5720465605:AAHf_wB4sFNdcjhQjf5_INs4MFeMUB6YyLg"