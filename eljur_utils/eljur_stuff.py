from utils import Database

import journal_api
from journal_api.api import Student
from journal_api.types import Lesson, Homework


from datetime import date, timedelta

from texttable import Texttable

import re



db = Database()

journal_api.api.dev_key = "d9ca53f1e47e9d2b9493d35e2a5e36"



async def create_token(user_id: int, login: str, password: str, force: bool = None) -> str | None:
    if force is True:
        token = await Student().authorization(login, password)
        db.insert_eljur_token(user_id, token)
        return token
    elif db.fetch_eljur_token(user_id):
        return None
    else:
        token = await Student().authorization(login, password)
        db.insert_eljur_token(user_id, token)
        return token


async def create_student(user_id: int) -> Student | None:
    token = db.fetch_eljur_token(user_id)
    if token:
        student = Student(auth_token=token)
        await student.auto_fill_data()
        return student
    else:
        return None


async def get_parsed_diary(student: Student, start_date: date, end_date: date) -> list:
    diary = (await student.get_diary(start_date,
                                    end_date))[:2]

    return diary


def parse_to_future(objects: [Lesson]) -> ([Lesson]):
    tomorrow = []
    day_after_tomorrow = []

    for obj in objects:
        if obj.date == date.today() + timedelta(days=1):
            tomorrow.append(obj)

        elif obj.date == date.today() + timedelta(days=2):
            day_after_tomorrow.append(obj)

    tomorrow.sort(key=lambda x: x.number)
    day_after_tomorrow.sort(key=lambda x: x.number)

    return tomorrow, day_after_tomorrow


def parse_homework_to_future(objects: [Homework]) -> ([Homework]):
    tomorrow = []
    day_after_tomorrow = []

    for obj in objects:
        if obj.date == date.today() + timedelta(days=1):
            tomorrow.append(obj)

        elif obj.date == date.today() + timedelta(days=2):
            day_after_tomorrow.append(obj)

    tomorrow.sort(key=lambda x: x.lesson_number)
    day_after_tomorrow.sort(key=lambda x: x.lesson_number)

    return tomorrow, day_after_tomorrow


def make_table(lessons: [Lesson]) -> str:
    table = Texttable()
    if not lessons:
        return 'В этот день уроков нет'
    for lesson in lessons:
        table.add_row([lesson.number, lesson.lesson, lesson.room])

    table.set_cols_align(['c', 'c', 'c'])

    table.header(['№', 'Урок', 'Кабинет'])

    table = table.draw()
    return table


def find_exercises(homework: Homework) -> [str]:
    exercises = re.findall(r'\b\d+\b', homework.text.strip())
    return exercises


async def do_eljur_stuff(user_id: int, start_date: date, end_date: date):
    student = await create_student(user_id)
    diary = await get_parsed_diary(student,
                                   start_date=start_date,
                                   end_date=end_date)

    lessons, homeworks = diary

    tomorrow, day_after_tomorrow = parse_to_future(lessons)

    table_tomorrow = str(date.today() + timedelta(days=1)) + '\n' + make_table(tomorrow)
    table_after_tomorrow = str(date.today() + timedelta(days=2)) + '\n' + make_table(day_after_tomorrow)

    print(table_tomorrow)
    print(table_after_tomorrow)

    for homework in homeworks:
        print(homework.lesson, homework.text.strip())
        print(find_exercises(homework))


async def parse_eljur(user_id: int, start_date: date, end_date: date):
    student = await create_student(user_id)
    diary = await get_parsed_diary(student,
                                   start_date=start_date,
                                   end_date=end_date)

    lessons, homeworks = diary
    tomorrow, day_after_tomorrow = parse_to_future(lessons)


    for homework in homeworks:
        pass


