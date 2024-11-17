import random
import git

from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from utils import Database


async def process_feedback(message: Message):
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

