import datetime
import logging
import sched
import time

from aiogram import Bot

import eljur_utils
from eljur_utils import find_exercises
from utils import get_russian, get_english, get_geometry, get_algebra, error_admin

logging.getLogger(__name__)


async def send_homework(users: list[int], bot: Bot):
    try:
        for user in users:
            student = await eljur_utils.create_student(user)
            await bot.send_message(user, 'Рассылка ГДЗ из ЭлЖура для VIP-пользователей')
            diary = await eljur_utils.get_parsed_diary(student,
                                           datetime.date.today() + datetime.timedelta(days=1),
                                           datetime.date.today() + datetime.timedelta(days=2))
            lessons, homeworks = diary
            tomorrow, day_after_tomorrow = eljur_utils.parse_to_future(lessons)

            table_tomorrow = (str(datetime.date.today() + datetime.timedelta(days=1)) +
                              '\n' + eljur_utils.make_table(tomorrow))

            table_after_tomorrow = (str(datetime.date.today() + datetime.timedelta(days=2)) +
                                    '\n' + eljur_utils.make_table(day_after_tomorrow))

            msgs = ['Расписания:', table_tomorrow, table_after_tomorrow]

            hw_tomorrow, hw_after_tomorrow = eljur_utils.parse_homework_to_future(homeworks)

            for hw in hw_tomorrow:
                try:
                    match hw.lesson:
                        case 'Алгебра':
                            exercises = find_exercises(hw)
                            for exercise in exercises:
                                msgs.append(get_algebra(exercise).build())
                                msgs.append(f'ГДЗ по Алгебре на {hw.date}, {exercise} задания')

                        case 'Геометрия':
                            exercises = find_exercises(hw)
                            for exercise in exercises:
                                msgs.append(get_geometry(exercise).build())
                                msgs.append(f'ГДЗ по Геометрии на {hw.date}, {exercise} задания')

                        case 'Русский язык':
                            exercises = find_exercises(hw)
                            for exercise in exercises:
                                msgs.append(get_russian(exercise).build())
                                msgs.append(f'ГДЗ по Русскому языку на {hw.date}, {exercise} задания')

                        case 'Иностранный язык (английский)':
                            exercises = find_exercises(hw)
                            for exercise in exercises:
                                msgs.append(get_english(exercise).build())
                                msgs.append(f'ГДЗ по Английскому языку на {hw.date}, {exercise} задания')
                except Exception as e:
                    logging.error(e)

            for hw in hw_after_tomorrow:
                try:
                    match hw.lesson:
                        case 'Алгебра':
                            exercises = find_exercises(hw)
                            for exercise in exercises:
                                msgs.append(get_algebra(exercise).build())
                                msgs.append(f'ГДЗ по Алгебре на {hw.date}, {exercise} задания')

                        case 'Геометрия':
                            exercises = find_exercises(hw)
                            for exercise in exercises:
                                msgs.append(get_geometry(exercise).build())
                                msgs.append(f'ГДЗ по Геометрии на {hw.date}, {exercise} задания')

                        case 'Русский язык':
                            exercises = find_exercises(hw)
                            for exercise in exercises:
                                msgs.append(get_russian(exercise).build())
                                msgs.append(f'ГДЗ по Русскому языку на {hw.date}, {exercise} задания')

                        case 'Иностранный язык (английский)':
                            exercises = find_exercises(hw)
                            for exercise in exercises:
                                msgs.append(get_english(exercise).build())
                                msgs.append(f'ГДЗ по Английскому языку на {hw.date}, {exercise} задания')
                except Exception as e:
                    logging.error(e)

                for message in msgs:
                    if isinstance(message, str):
                        await bot.send_message(user, message)
                    elif isinstance(message, list):
                        await bot.send_media_group(user, message)
                    else:
                        logging.warning('Unhandled message in utils.schedules.py' + str(type(message)))

    except Exception as e:
        logging.error(e)
