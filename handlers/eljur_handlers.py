import datetime

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from eljur_utils import create_student, create_token, get_parsed_diary, parse_to_future, make_table, find_exercises, \
    parse_homework_to_future
from utils import error_admin, get_algebra, get_geometry, get_russian, get_english, process_feedback
from utils.database import Database

eljur_router = Router()
database = Database()


@eljur_router.message(Command('token'))
async def get_token(message: Message, bot: Bot):
    try:
        student = await create_student(message.from_user.id)
        if student is None:
            await message.reply('У вас нет токена входа. Авторизоваться: /login логин пароль')
        else:
            await message.reply(f'У вас есть токен входа. Если проблемы со входом все же имеются, обратитесь к '
                                       f'<a href="https://t.me/rilliat">разработчику</a>\n'
                                       f'<tg-spoiler>{database.fetch_eljur_token(message.from_user.id)}</tg-spoiler>')
        await process_feedback(message)
    except Exception as e:
        await error_admin(bot, message, e)


@eljur_router.message(Command('login'))
async def login(message: Message, command: CommandObject, bot: Bot):
    try:
        student = await create_student(message.from_user.id)
        if student is None and not command.args:
            return await message.reply('Использование: /login логин пароль')
        elif not command.args:
            return await message.reply(
                'Использование: /login логин пароль. Если вы хотите обновить токен, обратитесь к '
                '<a href="https://t.me/rilliat">разработчику</a>')
        elif len(command.args.split()) == 2:
            await message.reply('Проводим попытку входа...')
            token = await create_token(message.from_user.id,
                                       command.args.split()[0],
                                       command.args.split()[1])
            if token is None:
                return await message.reply('Произошла какая-то ошибка...\n'
                                           'обратитесь к <a href="https://t.me/rilliat">разработчику</a>')
            await message.reply('Авторизация прошла успешно!\n'
                                       f'Ваш токен: '
                                       f'<tg-spoiler>{database.fetch_eljur_token(message.from_user.id)}</tg-spoiler> '
                                       f'(на самом деле он вам не понадобится)')
            await process_feedback(message)
        else:
            return await message.reply(
                'Использование: /login логин пароль. Если вы хотите обновить токен, обратитесь к '
                '<a href="https://t.me/rilliat">разработчику</a>')

    except Exception as e:
        await error_admin(bot, message, e)


@eljur_router.message(Command('homework'))
async def get_homework(message: Message, bot: Bot):
    try:
        msg = await message.reply('Подождите... Загружаем данные')

        student = await create_student(message.from_user.id)
        if student is None:
            return await msg.edit_text('У вас не подключён токен ЭлЖура. Пропишите /login')

        diary = await get_parsed_diary(student,
                                       datetime.date.today() + datetime.timedelta(days=1),
                                       datetime.date.today() + datetime.timedelta(days=2))
        lessons, homeworks = diary
        tomorrow, day_after_tomorrow = parse_to_future(lessons)

        table_tomorrow = (str(datetime.date.today() + datetime.timedelta(days=1)) +
                          '\n' + make_table(tomorrow))
        table_after_tomorrow = (str(datetime.date.today() + datetime.timedelta(days=2)) +
                                '\n' + make_table(day_after_tomorrow))

        await msg.edit_text('Расписания:')
        await message.reply(table_tomorrow)
        await message.reply(table_after_tomorrow)

        hw_tomorrow, hw_after_tomorrow = parse_homework_to_future(homeworks)

        for hw in hw_tomorrow:
            match hw.lesson:
                case 'Алгебра':
                    exercises = find_exercises(hw)
                    for exercise in exercises:
                        msg = await message.reply_media_group(get_algebra(exercise).build())
                        await msg[0].reply(f'ГДЗ по Алгебре на {hw.date}, {exercise} задания')

                case 'Геометрия':
                    exercises = find_exercises(hw)
                    for exercise in exercises:
                        msg = await message.reply_media_group(get_geometry(exercise).build())
                        await msg[0].reply(f'ГДЗ по Геометрии на {hw.date}, {exercise} задания')

                case 'Русский язык':
                    exercises = find_exercises(hw)
                    for exercise in exercises:
                        msg = await message.reply_media_group(get_russian(exercise).build())
                        await msg[0].reply(f'ГДЗ по Русскому языку на {hw.date}, {exercise} задания')

                case 'Иностранный язык (английский)':
                    exercises = find_exercises(hw)
                    for exercise in exercises:
                        msg = await message.reply_media_group(get_english(exercise).build())
                        await msg[0].reply(f'ГДЗ по Английскому языку на {hw.date}, {exercise} задания')

        for hw in hw_after_tomorrow:
            match hw.lesson:
                case 'Алгебра':
                    exercises = find_exercises(hw)
                    for exercise in exercises:
                        msg = await message.reply_media_group(get_algebra(exercise).build())
                        await msg[0].reply(f'ГДЗ по Алгебре на {hw.date}, {exercise} задания')

                case 'Геометрия':
                    exercises = find_exercises(hw)
                    for exercise in exercises:
                        msg = await message.reply_media_group(get_geometry(exercise).build())
                        await msg[0].reply(f'ГДЗ по Геометрии на {hw.date}, {exercise} задания')

                case 'Русский язык':
                    exercises = find_exercises(hw)
                    for exercise in exercises:
                        msg = await message.reply_media_group(get_russian(exercise).build())
                        await msg[0].reply(f'ГДЗ по Русскому языку на {hw.date}, {exercise} задания')

                case 'Иностранный язык (английский)':
                    exercises = find_exercises(hw)
                    for exercise in exercises:
                        msg = await message.reply_media_group(get_english(exercise).build())
                        await msg[0].reply(f'ГДЗ по Английскому языку на {hw.date}, {exercise} задания')

        await process_feedback(message)

    except Exception as e:
        await error_admin(bot, message, e)
