from dataclasses import dataclass

from aiogram import Dispatcher, Bot
from aiogram.types import Update


@dataclass
class BotDispatcher:
    bot: Bot
    dispatcher: Dispatcher


class FeederError(Exception):
    """Generic feeder error"""


class BotNotRegisteredError(FeederError):
    """No bot to feed update to"""


class Feeder:
    def __init__(self):
        self.bot_dispatcher_map: dict[int, BotDispatcher] = dict()

    def register(self, bot: Bot, dispatcher: Dispatcher):
        self.bot_dispatcher_map[bot.id] = BotDispatcher(bot, dispatcher)

    async def __call__(self, update: Update, bot_identifier: int):
        bot_dispatcher = self.bot_dispatcher_map.get(bot_identifier)
        if not bot_dispatcher:
            raise BotNotRegisteredError
        return await bot_dispatcher.dispatcher.feed_update(bot_dispatcher.bot, update)
