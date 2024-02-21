from contextlib import asynccontextmanager

from aiogram import Dispatcher, Bot
from dishka import (
    Provider,
    Scope,
    make_async_container,
    provide,
)
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from hhrubot.api.router.default import default_router
from hhrubot.api.router.webhook import webhook_router
from hhrubot.main.tg import create_hh_dispatcher, get_hh_bot


class TelegramObjectsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_dispatcher(self) -> Dispatcher:
        return create_hh_dispatcher()

    @provide(scope=Scope.APP)
    def get_bot(self) -> Bot:
        return get_hh_bot()


def include_routers(app: FastAPI):
    app.include_router(default_router)
    app.include_router(webhook_router)


def init_dependencies(app: FastAPI, dispatcher: Dispatcher, bot: Bot):
    app.dependency_overrides[Dispatcher] = lambda: dispatcher
    app.dependency_overrides[Bot] = lambda: bot


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def create_app():
    app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)
    include_routers(app)
    container = make_async_container(TelegramObjectsProvider())
    setup_dishka(container, app)
    return app
