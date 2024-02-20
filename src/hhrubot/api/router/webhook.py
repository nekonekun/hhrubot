from typing import Annotated

from aiogram import Dispatcher
from aiogram.types import Update
from fastapi import APIRouter, Depends

from hhrubot.api.depends_stub import Stub
from hhrubot.application.feeder import Feeder, FeederError


telegram_router = APIRouter(prefix='/webhook')


@telegram_router.post('/telegram/{bot_id}')
async def helloworld(
    bot_id: int,
    update: Update,
    feeder: Annotated[Feeder, Depends(Stub(Feeder))],
):
    try:
        return await feeder(update=update, bot_identifier=bot_id)
    except FeederError as exc:
        return None
