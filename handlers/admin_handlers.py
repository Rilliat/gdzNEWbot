from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils import *

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


db = Database()
admin_router = Router()


class AdminManager(StatesGroup):
    adding_user_id = State()
    removing_user_id = State()
    switching_valid_id = State()
    switching_vip_id = State()
    adding_token = State()
    switching_token = State()


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
    await call.message.edit_text(f'Avg callback:\n{db.check_callback()}', reply_markup=keyboard)


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
    await state.set_state(AdminManager.adding_user_id)
    await call.message.edit_text('Хорошо. Напишите ID пользователя:')


@admin_router.message(AdminManager.adding_user_id)
async def call_admin_add_user_choosed_id(message: Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Назад', callback_data='admin.menu')
    ]])
    await state.clear()
    if not message.text.isnumeric():
        return await message.reply('ID - не число!')

    db.add_user(int(message.text))
    await message.reply('Отлично! Добавлено в базу:\n'
                        f'ID: {message.text}\n'
                        f'Valid: True\n'
                        f'VIP: False', reply_markup=keyboard)


@admin_router.callback_query(F.data == 'admin.remove_user')
async def call_admin_remove_user(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(AdminManager.removing_user_id)


@admin_router.message(AdminManager.removing_user_id)
async def call_admin_remove_user_choosed_id(message: Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Назад', callback_data='admin.menu')
    ]])
    await state.clear()
    if not message.text.isnumeric():
        return await message.reply('ID - не число!')

    db.remove_user(int(message.text))
    await message.reply('Отлично! Удалено из базы:\n'
                        f'ID: {message.text}\n', reply_markup=keyboard)


@admin_router.callback_query(F.data == 'admin.switch_valid_user')
async def call_admin_switch_valid_user(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(AdminManager.switching_valid_id)


@admin_router.message(AdminManager.switching_valid_id)
async def call_admin_switch_valid_user_choosed_id(message: Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Назад', callback_data='admin.menu')
    ]])
    await state.clear()
    if not message.text.isnumeric():
        return await message.reply('ID - не число!')

    db.set_valid_user(int(message.text), not 1)
    await message.reply('ДОДЕЛАТЬ', reply_markup=keyboard)

