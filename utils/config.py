from dotenv import load_dotenv
import os

load_dotenv('.env')

api_token = str(os.getenv('API_TOKEN'))
admins = list(map(int, filter(None, str(os.getenv('ADMIN_IDS')).split(":"))))
database_name = str(os.getenv('DATABASE_NAME'))

