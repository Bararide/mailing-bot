import dbmanager as db

from config import router

from aiogram import types

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command

# Обработчик команды /start
@router.message(CommandStart())
async def handle_start(message: types.Message):
    await message.reply("Привет! Я простой Telegram-бот на aiogram для рассылки.")

# Обработчик команды /admin
@router.message(Command('admin'))
async def save_admin(message: types.Message):
    db.add_admin(message.from_user.id)
    await message.reply("Вы добавлены в список администраторов.")

# Обработчик команды /add_channel
@router.message(Command('add_channel'))
async def add_channel_command(message: types.Message):
    if len(message.text.split()) != 4:
        await message.reply("Неверное количество аргументов. Используйте команду /add_channel <channel_url> <channel_id> <chat_id>")
        return

    _, channel_url, channel_id, chat_id = message.text.split()
    db.add_channel(channel_url, channel_id, chat_id)
    await message.reply(f"Канал {channel_url} успешно добавлен.")

# Обработчик команды /menu
@router.message(Command('menu'))
async def show_menu(message: types.Message):
    channels = db.get_channels()

    if not channels:
        await message.reply("Список каналов пуст.")
        return

    keyboard_buttons = []
    for i, channel in enumerate(channels):
        button = InlineKeyboardButton(text=f"{i+1}. {channel[0]}", callback_data=f"delete_channel:{i}")
        keyboard_buttons.append([button])

    keyboard_buttons.append([InlineKeyboardButton(text="Вывести все группы/каналы", callback_data="show_all_channels")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons, row_width=1)  # Pass the list of button lists

    await message.reply("При нажатии на канал - канал будет удалён:", reply_markup=keyboard)
