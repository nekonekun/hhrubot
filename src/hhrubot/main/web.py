from contextlib import asynccontextmanager

from aiogram import Dispatcher, Bot
from fastapi import FastAPI

from hhrubot.api.router.default import default_router
from hhrubot.api.router.webhook import telegram_router
from hhrubot.application.feeder import Feeder
from hhrubot.main.tg import create_hh_dispatcher, get_hh_bot, init_bot, dispose_bot


def include_routers(app: FastAPI):
    app.include_router(default_router)
    app.include_router(telegram_router)


def init_dependencies(app: FastAPI, dispatcher: Dispatcher, bot: Bot):
    feeder = Feeder()
    feeder.register(bot, dispatcher)
    app.dependency_overrides[Feeder] = lambda: feeder


@asynccontextmanager
async def lifespan(app: FastAPI):
    include_routers(app)
    dispatcher = create_hh_dispatcher()
    bot = get_hh_bot()
    init_dependencies(app, dispatcher, bot)
    await dispatcher.emit_startup(bot=bot)
    yield
    await dispatcher.emit_shutdown(bot=bot)


def create_app():
    app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)
    return app
