from contextlib import asynccontextmanager

from fastapi import FastAPI

from hhrubot.api.router.default import default_router
from hhrubot.api.router.webhook import telegram_router
from hhrubot.application.feeder import Feeder
from hhrubot.main.tg import create_dispatcher, get_bots, set_webhooks


def include_routers(app: FastAPI):
    app.include_router(default_router)
    app.include_router(telegram_router)


def init_dependencies(app: FastAPI):
    dispatcher = create_dispatcher()
    bots = get_bots()
    feeder = Feeder(dispatcher, *bots)
    app.dependency_overrides[Feeder] = lambda: feeder


@asynccontextmanager
async def lifespan(app: FastAPI):
    bots = get_bots()
    await set_webhooks(*bots)
    yield


def create_app():
    app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)
    include_routers(app)
    init_dependencies(app)
    return app
