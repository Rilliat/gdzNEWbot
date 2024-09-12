import requests

from utils import *

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder


db = Database()
gdz_router = Router()


def findline(base_str: str, search_str: str) -> list[str]:
    return [x for x in base_str.splitlines() if search_str in x]


@gdz_router.message(Command('algebra'))
async def cmd_algebra(message: Message, command: CommandObject):
    if not command.args:
        return await message.reply('Нет аргументов!')
    if not command.args.isnumeric():
        return await message.reply('Аргумент - не число!')

    args = command.args.split()
    if len(args) > 1:
        return await message.reply('Пожалуйста, запрашивайте только 1 задание в 1 сообщении.')

    builder = MediaGroupBuilder(
        caption=f'Вот ваше ГДЗ для {args[0]} задания',
    )

    r = requests.get(f'https://gdz.ru/class-8/algebra/makarychev-8/{args[0]}-nom/')
    lines = findline(r.text, '<img src="//gdz.ru/attachments/images/tasks/000/005/968/0000/')

    for i_line in range(len(lines)):
        lines[i_line] = lines[i_line].strip().split('"')[1].split('//')[1]

    for gdz in lines:
        builder.add_photo(
            media='https://' + gdz,
        )
    await message.reply_media_group(builder.build())



@gdz_router.message(Command('hwsupports'))
async def cmd_hwsupports(message: Message):
    await message.answer(f'''Предметы, поддерживаемые командой /homework:
✅ Алгебра (100% готово)
❓ Геометрия (50% готово, в разработке)
❓ Физика (0% готово)
❓ Русский язык (0% готово)''')

