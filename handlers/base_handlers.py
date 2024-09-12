from utils import *

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from utils.misc import process_callback

db = Database()
base_router = Router()

# Хэндлер на команду /start
@base_router.message(CommandStart(deep_link=False))
async def cmd_start(message: Message):
    msg = ('Здравствуйте! Скелет клиента находится в разработке, сейчас в приоритете админ-часть.\n'
           'Все команды: /help'
           '\n\n{0}')

    admin_msg = 'Вы админ в данном боте.'

    if IsAdmin():
        msg = msg.format(admin_msg)
    else:
        msg = msg.format('')

    await message.reply(msg)
    await message.reply(f'Привет! Я - ГДЗ-бот, могу прислать тебе готовую домашку по некоторым предметам! \n'
                        f'Кстати, владелец - <a href="tg://user?id=1655585249">@rilliat</a>\n'
                        f'Для объяснения всех команд - добро пожаловать в /help :)')
    await process_callback(message)


@base_router.message(Command('help'))
async def cmd_help(message: Message):
    msg = ('Помощь по командам бота:\n'
           'TODO'
           '\n\n{0}')
    admin_msg = ('Админ-команды:\n'
                 'TODO')

    if IsAdmin():
        msg = msg.format(admin_msg)
    else:
        msg = msg.format('')

    await message.reply(msg)


@base_router.message(Command('todo'))
async def cmd_todo(message: Message):
    await message.reply('TODO:\n'
                        'todo')
