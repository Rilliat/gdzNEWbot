# Проверка минимальной версии Python (на 3.11 не работает из-за старых f-strings)
import sys
MIN_PYTHON = (3, 12)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

# Импорт утилит, роутеров, хэндлеров и т.д.
from utils import *
from handlers import *
from utils.misc import return_callback

# Импорт вспомогательных библиотек
import asyncio
import logging
from datetime import datetime

# Импорт объектов из aiogram
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import F


# Функции отправки сообщений о запуске и остановке бота админам
async def on_startup(bot: Bot, db: Database):
    for admin in admins:
        await bot.send_message(admin, f'Бот запущен!'
                                      f'\n\n<i>{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}</i>')

    # Настройка планировщика задач на рассылку ГДЗ VIP-пользователям
    users = db.fetch_vip_users()
    await scheduler(users, bot)


async def on_shutdown(bot: Bot):
    for admin in admins:
        await bot.send_message(admin, f'Бот остановлен!'
                                      f'\n\n<i>{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}</i>')


# Запуск процесса поллинга новых апдейтов
async def main():
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger(__name__)

    # Объект базы данных
    db = database.Database()
    # Первичная инициализация БД
    db.initialize()

    # Диспетчер
    dp = Dispatcher()

    # Объект бота
    bot = Bot(token=config.api_token,                                   # API-токен для подключения к боту
              default=DefaultBotProperties(parse_mode=ParseMode.HTML,   # HTML-режим форматирования
                                           protect_content=True),       # Отключение скриншотов, копирования и пересылки
              session=config.session)                                   # Подключение сессии (PRODUCTION или TEST)

    # Сброс накопленных за время простоя сообщений
    await bot.delete_webhook(drop_pending_updates=True)

    # Подключение роутеров из других файлов
    dp.include_routers(base_router, admin_router, gdz_router, eljur_router, no_access_router)

    # Подключение фильтра на корневой роутер (диспетчер)
    dp.update.filter(IsAllowed())

    # Подключение миддлвари логирования потому что да, а хули нет, я хочу чекать че пишут
    dp.update.outer_middleware(LoggingMiddleware())

    # Подключение фильтра на сообщения и инлайн-кнопки для админ-роутера
    admin_router.message.filter(IsAdmin())
    admin_router.callback_query.filter(IsAdmin())

    # Подключение функций отправки сообщения о старте и остановке бота админам
    dp['db'] = db
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Подключение функции слушания инлайн-кнопок для оценок бота в базовом роутере
    base_router.callback_query.register(return_callback, F.data.isnumeric())

    # Процесс поллинга новых апдейтов
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
