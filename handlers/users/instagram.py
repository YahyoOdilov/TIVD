from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
import json
from loader import dp
import requests

searching = 'qidirilmoqda...'
loading = 'yuklanmoqda...'
error_msg = 'kechirasiz bir xatolik yuz berdi, postni "private" emasligini tekshiring'


@dp.message_handler(Text(startswith= 'https://www.instagram.com/'))
async def instagram_downloader(msg: types.Message):
    url = "https://instagram-downloader-download-instagram-videos-stories.p.rapidapi.com/index"

    querystring = {"url":msg.text}

    headers = {
	    "X-RapidAPI-Key": "27505822b5mshed54f3b55d7eb53p1ae5bcjsnfe99e2627f66",
	    "X-RapidAPI-Host": "instagram-downloader-download-instagram-videos-stories.p.rapidapi.com"
    }
    state_msg = await msg.reply(searching)
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        await state_msg.edit_text(loading)
        data = json.loads(response.text)
        media = data['media']
        type = data['Type']
        loc_type, med_type = type.split('-')
        print(med_type, loc_type)
        title = data['title'] if loc_type == 'Post' else ''
        if med_type == 'Video':
            await msg.answer_video(media, caption= title)
        else:
            await msg.answer_photo(media, caption= title)
        await state_msg.delete()
    else:
        await state_msg.edit_text(error_msg)
        
    