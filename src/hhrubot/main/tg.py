import os

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage, Redis

from hhrubot.tg.router.echo import echo_router


def create_hh_dispatcher():
    dispatcher = Dispatcher(storage=RedisStorage(Redis()))
    dispatcher.include_router(echo_router)
    dispatcher.startup.register(init_bot)
    dispatcher.shutdown.register(dispose_bot)
    return dispatcher


def get_hh_bot():
    bot = Bot(token=os.getenv('HHRU_BOT_TOKEN'))
    return bot


async def init_bot(bot: Bot):
    url = os.getenv('HHRU_BOT_WEBHOOK_URL')
    await bot.set_webhook(url=url, allowed_updates=['message', 'callback_query', 'inline_query'])


async def dispose_bot(bot: Bot):
    await bot.session.close()
