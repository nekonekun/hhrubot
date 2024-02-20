import logging
import os

from aiogram import Dispatcher, Bot

from hhrubot.tg.router.echo import echo_router


def create_dispatcher():
    dispatcher = Dispatcher()
    dispatcher.include_router(echo_router)
    return dispatcher


def get_bots():
    bot = Bot(token=os.getenv('HHRU_BOT_TOKEN'))
    return [bot]


async def set_webhooks(*bots: Bot):
    url_prefix = os.getenv('HHRU_BOT_WEBHOOK_PREFIX')
    for bot in bots:
        await bot.set_webhook(url=url_prefix + str(bot.id))
