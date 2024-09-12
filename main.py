import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from utils import *
from handlers import *
from utils.misc import process_callback, return_callback

db = database.Database()

# Диспетчер
dp = Dispatcher()

async def on_startup(bot: Bot):
    for admin in admins:
        await bot.send_message(admin, f'Бот запущен!'
                                      f'\n\n<i>{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}</i>')

async def on_shutdown(bot: Bot):
    for admin in admins:
        await bot.send_message(admin, f'Бот остановлен!'
                                      f'\n\n<i>{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}</i>')


# Запуск процесса поллинга новых апдейтов
async def main():
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)

    # Объект бота
    bot = Bot(token=config.api_token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML,
                                           protect_content=True))

    # Сброс накопленных за время простоя сообщений
    await bot.delete_webhook(drop_pending_updates=True)
    # Подключение роутеров из других файлов
    dp.include_routers(base_router, admin_router, gdz_router)

    # Подключение необходимых фильтров на роутеры
    base_router.message.filter(IsAllowed())
    gdz_router.message.filter(IsAllowed())

    admin_router.message.filter(IsAdmin())
    admin_router.callback_query.filter(IsAdmin())

    # Подключение функций отправки сообщения о старте и остановке бота админам
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    base_router.callback_query.register(return_callback)

    # Процесс поллинга новых апдейтов
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
