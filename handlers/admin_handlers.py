from utils import *

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


db = Database()
admin_router = Router()

@admin_router.message(Command('admin'))
async def cmd_admin(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Статистика', callback_data='admin.stats'),
        InlineKeyboardButton(text='Пользователи', callback_data='admin.users')
    ]])
    await message.reply('admin panel: todo', reply_markup=keyboard)


@admin_router.callback_query(F.data == 'admin.menu')
async def call_admin_menu(call: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Статистика', callback_data='admin.stats'),
        InlineKeyboardButton(text='Пользователи', callback_data='admin.users')
    ]])
    await call.message.edit_text('admin panel: todo', reply_markup=keyboard)


@admin_router.callback_query(F.data == 'admin.stats')
async def call_admin_stats(call: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Назад', callback_data='admin.menu')
    ]])
    await call.message.edit_text(f'Admin panel:\nAvg callback:\n{db.check_callback()}', reply_markup=keyboard)


@admin_router.callback_query(F.data == 'admin.users')
async def call_admin_users(call: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Назад', callback_data='admin.menu')
    ]])
    await call.message.edit_text(f'Admin panel:\nUsers:\n{db.check_users()}\n'
                                 f'Valid users: {db.check_users(valid=True)}\n'
                                 f'Vip users: {db.check_users(vip=True)}', reply_markup=keyboard)