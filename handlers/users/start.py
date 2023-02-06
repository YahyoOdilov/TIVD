from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.db_api.user import User

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    tid = message.from_user.id
    username = message.from_user.username
    username = '@' + username if username else message.from_user.full_name
    user = User.get(tid = tid)
    if not user:
        user = User.insert(tid= tid, username = username)
    await message.answer(f"Salom, {username}!\n<b>TIVDbot</b>ga hush kelibsiz\n\nO'zingiz yoqtirgan tiktok yoki instagram video/rasm linkini tashlang")
