from utils import *

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from utils.misc import process_feedback

db = Database()
base_router = Router()

# Хэндлер на команду /start
@base_router.message(CommandStart(deep_link=False))
async def cmd_start(message: Message):
    msg = ('Здравствуйте! Вас приветствует ГДЗ-бот от <a href="https://t.me/rilliat>Rilliat</a>.\n'
           'Все команды: /help'
           '\n\n{0}')

    admin_msg = 'Вы админ в данном боте.'

    if IsAdmin():
        msg = msg.format(admin_msg)
    else:
        msg = msg.format('')

    await message.reply(msg)
    await process_feedback(message)


@base_router.message(Command('help'))
async def cmd_help(message: Message):
    msg = ('Помощь по командам бота:\n'
           '<code>/start</code> - (пере)запустить бота\n'
           '<code>/help</code> - показать это сообщение\n'
           '<code>/todo</code> - TODO-список (список целей и задач)\n'
           '\n'
           '<code>/algebra номер</code> - ГДЗ по алгебре на нужный номер\n'
           '<code>/geometry номер</code> - ГДЗ по геометрии на нужный номер\n'
           '<code>/physics номер/ДОП/подномер</code> - ГДЗ по физике. Смотрите /physics для подробностей\n'
           '<code>/russian номер</code> - ГДЗ по русскому языку на нужное упр-е\n'
           '<code>/english номер</code> - ГДЗ по английскому языку на нужную страницу\n'
           '\n'
           '<code>/hwsupports</code> - список поддерживаемых ботом предметов\n'
           '<code>/login логин пароль</code> - войти в ЭлЖур\n'
           '<code>/token</code> - проверить токен ЭлЖура\n'
           '<code>/homework</code> - команда для вызова расписаний на 2 предстоящих дня и '
           'ГДЗ по поддерживаемым предметам\n'
           '\n\n{0}')
    admin_msg = ('Админ-команды:\n'
                 '/admin - админ-панель')

    if IsAdmin():
        msg = msg.format(admin_msg)
    else:
        msg = msg.format('')

    await message.reply(msg)


@base_router.message(Command('todo'))
async def cmd_todo(message: Message):
    await message.reply('TODO:\n'
                        '✅ v3\n'
                        '❌ Добавить другие предметы'
                        '❌ Реализовать систему автодобавления юзера по токену'
                        '❌ Багофикс\n'
                        '❌ Другое\n'
)
