import asyncio

import telethon.tl.types
from telethon import utils
from telethon.sync import TelegramClient, events
import settings
import logging
import magic
from functions.embend_handler import CheckContent

magic = magic.Magic(mime=True)
bot = TelegramClient('bot', settings.api_id, settings.api_hash).start(
    bot_token=settings.bot_token)

checkContent = CheckContent(bot)


@bot.on(events.NewMessage())
async def handler(event):
    if event.message.file:
        await checkContent.check_events(event)


bot.run_until_disconnected()
