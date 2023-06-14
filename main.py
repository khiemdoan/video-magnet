
__author__ = 'Khiem Doan'
__github__ = 'https://github.com/khiemdoan'
__email__ = 'doankhiem.crazy@gmail.com'

import asyncio
import logging
import re

import httpx
from telegram import Message, Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from yt_dlp import YoutubeDL

from decorators import ignore_exception_with_logger
from settings import get_telegram_settings

logger = logging.getLogger(__name__)

settings = get_telegram_settings()

ydl = YoutubeDL()

@ignore_exception_with_logger(logger)
async def fetch_video(in_message: Message, url: str) -> None:
    info = await asyncio.to_thread(ydl.extract_info, url, download=False)

    duration = info['duration']
    caption = info['title'][:500]
    thumbnail_url = info['thumbnails'][-1]['url']
    formats = [f for f in info['formats'] if f.get('acodec') != 'none' and f.get('vcodec') != 'none']
    format = formats[len(formats) // 2]

    if duration > 1800:
        print(f'Video is too long: {duration}s')
        return

    async with httpx.AsyncClient(follow_redirects=True) as client:
        thumbnail = await client.get(thumbnail_url)
        video = await client.get(format['url'])

    await in_message.reply_video(video=video.content, duration=duration, caption=caption, thumbnail=thumbnail.content)


PATTERN = re.compile(r'(https?://\S+)')

async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    urls = PATTERN.findall(update.message.text)
    tasks = [fetch_video(update.message, u) for u in urls]
    await asyncio.gather(*tasks)


def main() -> None:
    app = Application.builder().token(settings.bot_token).build()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.bot.initialize())

    name = loop.run_until_complete(app.bot.get_my_name())
    print(f'{name} is ready!')

    app.add_handler(MessageHandler(filters.TEXT, process_message, block=False))
    app.run_polling(allowed_updates=Update.CHAT_MEMBER)


if __name__ == '__main__':
    main()
