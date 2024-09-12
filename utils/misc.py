import random

from aiogram import Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from utils import admins, Database


async def error_admin(bot: Bot, message: Message, err):
    try:
        for admin in admins:
            try:
                await message.forward(admin)
            except Exception as e:
                await bot.send_message(admin, str(e))
            await bot.send_message(admin, str(err))
    except Exception as e:
        print(e)


async def process_callback(message: Message):
    if random.randint(1, 5) == 1:
        keyboard = [[InlineKeyboardButton(text='1 ⭐', callback_data='1'),
                     InlineKeyboardButton(text='2 ⭐', callback_data='2'),
                     InlineKeyboardButton(text='3 ⭐', callback_data='3')],
                    [InlineKeyboardButton(text='4 ⭐', callback_data='4'),
                     InlineKeyboardButton(text='5 ⭐', callback_data='5')]]

        feedback_inline_kb = InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)
        await message.reply('''Пожалуйста, оцените работу бота. Вам быстро, а мне приятно :)''',
                             reply_markup=feedback_inline_kb)
    else:
        return False


async def return_callback(call: CallbackQuery):
    database = Database()
    database.insert_callback(call.from_user.id, int(call.data))
    await call.answer()
    await call.message.reply('Принято: {0} ⭐'.format(int(call.data)))
    await call.message.delete()

