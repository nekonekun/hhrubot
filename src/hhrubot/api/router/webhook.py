from typing import Annotated

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from dishka.integrations.fastapi import Depends, inject
from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

from hhrubot.application.headhunter import AuthenticateUser

webhook_router = APIRouter(prefix='/webhook')


@webhook_router.post('/telegram/')
@inject
async def handle_update(
    update: Update,
    dispatcher: Annotated[Dispatcher, Depends()],
    bot: Annotated[Bot, Depends()],
):
    return await dispatcher.feed_webhook_update(bot, update)


@webhook_router.get('/headhunter/{telegram_id}/')
@inject
async def handle_authentication(
    telegram_id: int,
    code: Annotated[str, Query()],
    bot: Annotated[Bot, Depends()],
    authenticate_user: Annotated[AuthenticateUser, Depends()]
):
    await authenticate_user(telegram_id, code)
    await bot.send_message(telegram_id, 'Successfully authenticated.')
    return JSONResponse(content={'whats next': 'close window'}, status_code=status.HTTP_200_OK)
