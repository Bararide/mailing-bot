import aiogram

from aiogram import Bot, Dispatcher
from aiogram import Router

bot_token = 'BOT_API_KEY'
bot = Bot(token=bot_token)
router = Router()
dp = Dispatcher()
dp.include_router(router)
