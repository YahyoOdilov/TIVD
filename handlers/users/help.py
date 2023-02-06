from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Bu bot siz yoqtirgan Tiktok yoki Instagramdan video/rasmlar yuklash uchun yordam beradi",
            "O'zingiz yoqtirgan video/rasm linkini tashlang")
    
    await message.answer("\n\n".join(text))
