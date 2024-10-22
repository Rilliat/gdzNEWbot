from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.session.base import BaseSession
from aiogram.client.telegram import PRODUCTION, TEST
from dotenv import load_dotenv
import os

load_dotenv('.env')

api_token = str(os.getenv('API_TOKEN') if str(os.getenv('TEST_BOT')) == 'False'
                else str(os.getenv('TEST_API_TOKEN')))
admins = list(map(int, filter(None, str(os.getenv('ADMIN_IDS')).split(":"))))
database_name = str(os.getenv('DATABASE_NAME'))

testing_environment = True if str(os.getenv('TEST_BOT')) == 'True' else False
admins = (list(map(int, filter(None, str(os.getenv('TEST_ADMIN_IDS')).split(":"))))
          if testing_environment is True
          else admins)

api = PRODUCTION if testing_environment is False else TEST
session = AiohttpSession(api=api)

