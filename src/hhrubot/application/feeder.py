import random

from aiogram import Dispatcher, Bot
from aiogram.types import Update


class FeederError(Exception):
    """Generic feeder error"""


class BotNotRegisteredError(Exception):
    """No bot to feed update to"""


class Feeder:
    def __init__(self, dispatcher: Dispatcher, *bots: Bot):
        self.dispatcher = dispatcher
        self.bots = bots

    async def __call__(self, update: Update, bot_identifier: str | None = None):
        if len(self.bots) == 1:
            target_bot = self.bots[0]
        elif not bot_identifier:
            target_bot = random.choice(self.bots)
        else:
            target_bot = list(filter(lambda x: x.id == bot_identifier, self.bots))
            if not target_bot:
                raise BotNotRegisteredError
            target_bot = target_bot[0]
        return await self.dispatcher.feed_update(bot=target_bot, update=update)
