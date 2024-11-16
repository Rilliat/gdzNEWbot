from utils import IsAllowed

from aiogram import Router
from aiogram.types import Message


no_access_router = Router()

# Хэндлер на отсутствие команды
@no_access_router.message(IsAllowed())
async def cmd_404(message: Message):
    await message.reply(f'Команда <code>{message.text}</code> не найдена.')


# Хэндлер на отсутствие доступа
@no_access_router.message(~IsAllowed())
async def cmd_no_access(message: Message):
    await message.reply('У вас нет доступа. Приобрести - <a href="https://t.me/rilliat">Rilliat</a>.\n'
                        '<b>Цены:</b>\n'
                        'Базовый доступ - 50₽/мес. (скидка 20% при покупке от 2 месяцев)\n'
                        'VIP-доступ (автоотправка ГДЗ, приоритет в помощи,...) - дополнительно 20₽/мес. (скидка 25% при покупке от 2 мес.)\n'
                        '\n'
                        'Какие-то проблемы? Пишите <a href="https://t.me/rilliat">Rilliat</a>.')