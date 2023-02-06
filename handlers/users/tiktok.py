from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
import json
from loader import dp
import requests
from .instagram import searching, loading, error_msg

@dp.message_handler(Text(startswith= 'https://www.tiktok.com/'))
async def tiktok_downloader(msg: types.Message):
    url = "https://tiktok-downloader-download-tiktok-videos-without-watermark.p.rapidapi.com/vid/index"

    querystring = {"url":{msg.text}}

    headers = {
	    "X-RapidAPI-Key": "27505822b5mshed54f3b55d7eb53p1ae5bcjsnfe99e2627f66",
	    "X-RapidAPI-Host": "tiktok-downloader-download-tiktok-videos-without-watermark.p.rapidapi.com"
    }
    state_msg = await msg.reply(searching)
    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == 200:
        await state_msg.edit_text(loading)
        data = json.loads(response.text)
        videos = data['video']
        for video in videos:
            await msg.reply_video(video)
        await state_msg.delete()
    else:
        await state_msg.edit_text(error_msg)