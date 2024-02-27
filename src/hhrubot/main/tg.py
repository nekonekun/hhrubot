import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import Redis, RedisStorage
from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.aiogram import setup_dishka

from hhrubot.adapter.redisgram import RedisGram
from hhrubot.tg.middleware.employee import EmployeeMiddleware
from hhrubot.tg.router.echo import echo_router
from hhrubot.tg.router.resume import resume_router
from hhrubot.tg.router.greeting import greeting_router
from .providers import (
    HeadhunterMethodsProvider,
    HeadhunterOfflineProvider,
    HeadhunterOnlineProvider,
)


async def create_hh_dispatcher():
    dispatcher = Dispatcher(storage=RedisStorage(Redis()))
    dispatcher.include_router(greeting_router)
    dispatcher.include_router(resume_router)
    dispatcher.include_router(echo_router)
    dispatcher.startup.register(init_bot)
    dispatcher.shutdown.register(dispose_bot)
    container = make_async_container(
        HeadhunterOfflineProvider(),
        HeadhunterOnlineProvider(),
        HeadhunterMethodsProvider(),
    )
    setup_dishka(container, dispatcher)
    employee_middleware = EmployeeMiddleware()
    dispatcher.message.middleware(employee_middleware)
    dispatcher.callback_query.middleware(employee_middleware)
    return dispatcher


def get_hh_bot():
    return Bot(token=os.getenv('HHRU_BOT_TOKEN'))


async def init_bot(bot: Bot):
    url = os.getenv('HHRU_BOT_WEBHOOK_URL')
    await bot.set_webhook(
        url=url,
        allowed_updates=['message', 'callback_query', 'inline_query'],
        drop_pending_updates=True,
    )


async def dispose_bot(bot: Bot):
    await bot.session.close()


class TelegramObjectsProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_dispatcher(self) -> Dispatcher:
        return await create_hh_dispatcher()

    @provide(scope=Scope.APP)
    def get_bot(self) -> Bot:
        return get_hh_bot()

    @provide(scope=Scope.APP)
    def get_redisgram(self, dispatcher: Dispatcher, bot: Bot) -> RedisGram:
        storage = dispatcher.storage
        return RedisGram(storage=storage, bot_id=bot.id)
