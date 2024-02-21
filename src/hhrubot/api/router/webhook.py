from typing import Annotated

from aiogram import Dispatcher, Bot
from aiogram.types import Update
from dishka.integrations.fastapi import Depends, inject
from fastapi import APIRouter


webhook_router = APIRouter(prefix='/webhook')


@webhook_router.post('/telegram/')
@inject
async def handle_update(
    update: Update,
    dispatcher: Annotated[Dispatcher, Depends()],
    bot: Annotated[Bot, Depends()],
):
    return await dispatcher.feed_update(bot, update)
