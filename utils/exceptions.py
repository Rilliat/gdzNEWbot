from aiogram import Bot
from aiogram.types import Message

from utils import admins


async def error_admin(bot: Bot, message: Message, err):
    try:
        for admin in admins:
            try:
                await message.forward(admin)
            except Exception as e:
                await bot.send_message(admin, str(e))
            await message.reply(f'Извините, произошла непредвиденная ошибка '
                                f'{err}. Администратор уже получил об этом информацию, '
                                f'ждите фикса :) ')
            await bot.send_message(admin, str(err))
    except Exception as e:
        print(e)



