from typing import Annotated

from aiogram import Dispatcher, Bot
from aiogram.types import Update
from fastapi import APIRouter, Depends

from hhrubot.api.depends_stub import Stub


telegram_router = APIRouter(prefix='/webhook')


@telegram_router.post('/telegram/')
async def handle_update(
    update: Update,
    dispatcher: Annotated[Dispatcher, Depends(Stub(Dispatcher))],
    bot: Annotated[Bot, Depends(Stub(Bot))],
):
    return await dispatcher.feed_update(bot, update)
