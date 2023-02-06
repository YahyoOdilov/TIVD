from time import sleep
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.db_api.user import User

from loader import dp


@dp.message_handler()
async def bot_start(message: types.Message):
    username = message.from_user.username
    username = '@' + username if username else message.from_user.full_name
    await message.answer(f"kechirasiz, {username}. Bu bot faqat Instagram va tiktok medialarini yuklash uchun!")