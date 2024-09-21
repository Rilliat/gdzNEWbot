import requests

from utils import *

from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder


db = Database()
gdz_router = Router()


def findline(base_str: str, search_str: str) -> list[str]:
    return [x for x in base_str.splitlines() if search_str in x]


def findgdz(link: str, image_src: str, caption: str, additional: str  = None) -> MediaGroupBuilder:
    builder = MediaGroupBuilder(
        caption=caption
    )

    page = requests.get(link).text
    lines = findline(page, '<img src="' + image_src)

    for index in range(len(lines)):
        lines[index] = lines[index].strip().split('"')[1]
        lines[index] = lines[index].replace('//', '')
        if lines[index][0] == '/':
            lines[index] = lines[index][1:]

    for image in lines:
        if additional:
            image = additional + image
        image = image.replace('https:', '').replace('//', '')
        if 'https://' not in image:
            builder.add_photo(
                media='https://' + image
            )

    return builder


@gdz_router.message(Command('algebra'))
async def cmd_algebra(message: Message, command: CommandObject, bot: Bot):
    try:
        if not command.args:
            return await message.reply('Нет аргументов!')
        if not command.args.isnumeric():
            return await message.reply('Аргумент - не число!')

        args = command.args.split()
        if len(args) > 1:
            return await message.reply('Пожалуйста, запрашивайте только 1 задание в 1 сообщении.')


        await message.reply_media_group(findgdz(f'https://gdz.ru/class-8/algebra/makarychev-8/{args[0]}-nom/',
                                                '//gdz.ru/attachments/images/tasks/000/005/968/0000/',
                                                f'Вот ваше ГДЗ для {args[0]} задания по Алгебре').build())
    except Exception as e:
        await error_admin(bot, message, e)


@gdz_router.message(Command('geometry'))
async def cmd_geometry(message: Message, command: CommandObject, bot: Bot):
    try:
        if not command.args:
            return await message.reply('Нет аргументов!')
        if not command.args.isnumeric():
            return await message.reply('Аргумент - не число!')

        args = command.args.split()
        if len(args) > 1:
            return await message.reply('Пожалуйста, запрашивайте только 1 задание в 1 сообщении.')

        await message.reply_media_group(findgdz(f'https://gdz.top/7-klass/geometrija/atanasjan-fgos/{args[0]}',
                                                '/geometrija_07/atanasjan-fgos/1-00/',
                                                f'Вот ваше ГДЗ для {args[0]} задания по Геометрии',
                                                'gdz.top/').build())
    except Exception as e:
        await error_admin(bot, message, e)


@gdz_router.message(Command('physics'))
async def cmd_physics(message: Message, command: CommandObject, bot: Bot):
    try:
        if not command.args or len(command.args.split()) == 1:
            return await message.reply('Нет аргументов! Использование: <code>/physics номер пар/упр/зад/лаб/обс/'
                                       'задача *подномер</code>\n'
                                       'Пояснения: \n'
                                       'пар-параграф. /physics номер пар\n'
                                       'упр-упражнение. /physics номер упр подномер\n'
                                       'зад-задание. /physics номер_параграфа зад\n'
                                       'лаб-лабораторная работа. /physics номер лаб\n'
                                       'обс-обсуди с товарищами. /physics номер_параграфа обс\n'
                                       'задача-задача для повторения. /physics номер задача')
        args = command.args.split()

        if not args[0].isnumeric():
            return await message.reply('Первый аргумент - не число!')

        if len(args) > 3:
            return await message.reply('Пожалуйста, запрашивайте только 1 задание в 1 сообщении. ')

        if args[1] not in ['пар', 'упр', 'зад', 'лаб', 'обс', 'задача']:
            return await message.reply(
                'Использование: <code>/physics номер пар/упр/зад/лаб/обс/'
                'задача *подномер</code>\n'
                'Пояснения: \n'
                'пар-параграф. /physics номер пар\n'
                'упр-упражнение. /physics номер упр подномер\n'
                'зад-задание. /physics номер_параграфа зад\n'
                'лаб-лабораторная работа. /physics номер лаб\n'
                'обс-обсуди с товарищами. /physics номер_параграфа обс\n'
                'задача-задача для повторения. /physics номер задача')

        builder = MediaGroupBuilder(
            caption=f'Вот ваше ГДЗ по Физике',
        )

        try:
            match args[1]:
                case 'пар':
                    builder = findgdz(f'https://megaresheba.ru/index/05/0-358/{args[0]}',
                                      'https://megaresheba.ru/attachments/images/tasks/000/003/672/0000/654b5',
                                      f'Вот ваше гдз для {args[0]} параграфа по Физике')
                case 'упр':
                    builder = findgdz(f'https://megaresheba.ru/index/05/0-358/2-{args[0]}-{args[2]}',
                                      'https://megaresheba.ru/attachments/images/tasks/000/003/672/0000/654b5',
                                      f'Вот ваше гдз для {args[0]} упражнения подномер {args[2]} по Физике')
                case 'зад':
                    builder = findgdz(f'https://megaresheba.ru/index/05/0-358/3-{args[0]}',
                                      'https://megaresheba.ru/attachments/images/tasks/000/003/672/0000/654b5',
                                      f'Вот ваше гдз для задания из параграфа {args[0]} по Физике')
                case 'лаб':
                    builder = findgdz(f'https://megaresheba.ru/index/05/0-358/5-{args[0]}',
                                      'https://megaresheba.ru/attachments/images/tasks/000/003/672/0000/654b5',
                                      f'Вот ваше гдз для лабораторной работы {args[0]} по Физике')
                case 'обс':
                    builder = findgdz(f'https://megaresheba.ru/index/05/0-358/6-{args[0]}',
                                      'https://megaresheba.ru/attachments/images/tasks/000/003/672/0000/654b5',
                                      f'Вот ваше гдз для "обсуди с товарищами" из параграфа {args[0]} по Физике')
                case 'задача':
                    builder = findgdz(f'https://megaresheba.ru/index/05/0-358/7-{args[0]}',
                                      'https://megaresheba.ru/attachments/images/tasks/000/003/672/0000/654b5',
                                      f'Вот ваше гдз для задачи {args[0]} по Физике')

        except IndexError:
            await message.reply(
                'Использование: <code>/physics номер пар/упр/зад/лаб/обс/'
                'задача *подномер</code>\n'
                'Пояснения: \n'
                'пар-параграф. /physics номер пар\n'
                'упр-упражнение. /physics номер упр подномер\n'
                'зад-задание. /physics номер_параграфа зад\n'
                'лаб-лабораторная работа. /physics номер лаб\n'
                'обс-обсуди с товарищами. /physics номер_параграфа обс\n'
                'задача-задача для повторения. /physics номер задача')


        await message.reply_media_group(builder.build())

    except Exception as e:
        await error_admin(bot, message, e)



@gdz_router.message(Command('hwsupports'))
async def cmd_hwsupports(message: Message):
    await message.answer(f'''Предметы, поддерживаемые командой /homework:
✅ Алгебра (100% готово)
✅ Геометрия (100% готово)
✅ Физика (100% готово)
❓ Русский язык (0% готово)
❓ Английский язык (0% готово)
❓ (0% готово)
❓ (0% готово)''')

