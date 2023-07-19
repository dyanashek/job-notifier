import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
BOT_ID = os.getenv('BOT_ID')
MANAGER_ID = os.getenv('MANAGER_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')

SPREAD_NAME = os.getenv('SPREAD_NAME')
LIST_NAME = os.getenv('LIST_NAME')

ON_PAGE = int(os.getenv('ON_PAGE'))

START_MESSAGE = 'Hello world!'