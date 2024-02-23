from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka as setup_dishka
from fastapi import FastAPI

from hhrubot.api.router.default import default_router
from hhrubot.api.router.webhook import webhook_router
from hhrubot.api.router.internal import internal_router

from .providers import HeadhunterOfflineProvider, HeadhunterOnlineProvider, HeadhunterMethodsProvider
from .tg import TelegramObjectsProvider


def include_routers(app: FastAPI):
    app.include_router(default_router)
    app.include_router(webhook_router)
    app.include_router(internal_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    dispatcher: Dispatcher = await app.state.dishka_container.get(Dispatcher)
    bot: Bot = await app.state.dishka_container.get(Bot)
    await dispatcher.emit_startup(bot=bot)
    yield
    await dispatcher.emit_shutdown(bot=bot)
    await app.state.dishka_container.close()


def create_app():
    app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)
    include_routers(app)
    container = make_async_container(
        TelegramObjectsProvider(),
        HeadhunterOfflineProvider(),
        HeadhunterOnlineProvider(),
        HeadhunterMethodsProvider()
    )
    setup_dishka(container, app)
    return app
