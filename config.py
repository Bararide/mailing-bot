import aiogram

from aiogram import Bot, Dispatcher
from aiogram import Router

bot_token = '6723627717:AAHgE8qL5Y1n8VUvE6oVYnUozh04frc7bFA'
bot = Bot(token=bot_token)
router = Router()
dp = Dispatcher()
dp.include_router(router)