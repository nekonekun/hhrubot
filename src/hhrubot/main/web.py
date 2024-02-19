from fastapi import FastAPI

from hhrubot.api.router.default import default_router


def include_routers(app: FastAPI):
    app.include_router(default_router)


def create_app():
    app = FastAPI(docs_url=None, redoc_url=None)
    include_routers(app)
    return app
