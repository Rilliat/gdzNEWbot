from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils import *

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


db = Database()
admin_router = Router()


class AdminAddingUser(StatesGroup):
    choosing_id = State()


@admin_router.message(Command('admin'))
async def cmd_admin(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Статистика', callback_data='admin.stats'),
        InlineKeyboardButton(text='Пользователи', callback_data='admin.users')], [
        InlineKeyboardButton(text='Добавить пользователя', callback_data='admin.add_user'),
        InlineKeyboardButton(text='Удалить пользователя', callback_data='admin.remove_user')], [
        InlineKeyboardButton(text='Переключить валидность', callback_data='admin.switch_valid_user'),
        InlineKeyboardButton(text='Переключить VIP', callback_data='admin.switch_vip_user')],[
        InlineKeyboardButton(text='Добавить токен', callback_data='admin.add_token'),
        InlineKeyboardButton(text='Переключить валидность токена', callback_data='admin.switch_valid_token')
    ]])
    await message.reply('Админ-панель', reply_markup=keyboard)


@admin_router.callback_query(F.data == 'admin.menu')
async def call_admin_menu(call: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Статистика', callback_data='admin.stats'),
        InlineKeyboardButton(text='Пользователи', callback_data='admin.users')], [
        InlineKeyboardButton(text='Добавить пользователя', callback_data='admin.add_user'),
        InlineKeyboardButton(text='Удалить пользователя', callback_data='admin.remove_user')], [
        InlineKeyboardButton(text='Переключить валидность', callback_data='admin.switch_valid_user'),
        InlineKeyboardButton(text='Переключить VIP', callback_data='admin.switch_vip_user')], [
        InlineKeyboardButton(text='Добавить токен', callback_data='admin.add_token'),
        InlineKeyboardButton(text='Переключить валидность токена', callback_data='admin.switch_valid_token')
    ]])
    await call.message.edit_text('Админ-панель', reply_markup=keyboard)


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


@admin_router.callback_query(F.data == 'admin.add_user')
async def call_admin_add_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminAddingUser.choosing_id)
    await call.message.edit_text('Хорошо. Напишите ID пользователя:')

@admin_router.callback_query(AdminAddingUser.choosing_id)
async def call_admin_add_user_choosed_id(message: Message, state: FSMContext):
    await state.clear()
    if not message.text.isnumeric():
        return await message.reply('ID - не число!')

    db.add_user(int(message.text))
    await message.reply('Отлично! Добавлено в базу:\n'
                        f'ID: {message.text}\n'
                        f'Valid: True\n'
                        f'VIP: False')





