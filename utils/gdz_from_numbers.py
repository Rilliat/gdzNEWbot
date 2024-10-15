import requests
from aiogram.utils.media_group import MediaGroupBuilder


def findline(base_str: str, search_str: str) -> list[str]:
    return [x for x in base_str.splitlines() if search_str in x]


def findgdz(link: str, image_src: str, caption: str, additional: str = None) -> MediaGroupBuilder:
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


def get_algebra(num: str) -> MediaGroupBuilder:
    return findgdz(f'https://gdz.ru/class-8/algebra/makarychev-8/{num}-nom/',
            '//gdz.ru/attachments/images/tasks/000/005/968/0000/',
            f'Вот ваше ГДЗ для {num} задания по Алгебре')


def get_geometry(num: str) -> MediaGroupBuilder:
    return findgdz(f'https://gdz.top/7-klass/geometrija/atanasjan-fgos/{num}',
                   '/geometrija_07/atanasjan-fgos/3-00/',
                   f'Вот ваше ГДЗ для {num} задания по Геометрии',
                   'gdz.top/')


def get_russian(num: str) -> MediaGroupBuilder:
    return findgdz(f'https://megaresheba.ru/publ/reshebnik/russkomu_jazyku/barkhudarov_8_klass/35-1-0-1220/{num}',
                   'https://megaresheba.ru/attachments/images/tasks/000/003/491/0000/64faf',
                   f'Вот ваше ГДЗ для {num} задания по Русскому языку')


def get_english(num: str) -> MediaGroupBuilder:
    return findgdz(f'https://megaresheba.ru/index/sru8_eng4/0-4588/1-{num}',
                   'https://megaresheba.ru/attachments/images/tasks/000/003/579/0000/64fe3',
                   f'Вот ваше ГДЗ для {num} страницы по Английскому языку')

