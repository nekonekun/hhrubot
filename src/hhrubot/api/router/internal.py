import asyncio
from pathlib import Path
from typing import Annotated

from aiogram import Bot
from aiogram.types import FSInputFile
from dishka.integrations.fastapi import Depends, inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

internal_router = APIRouter(prefix='/internal')


class SendDocumentsRequest(BaseModel):
    telegram_id: int
    filename: str


@internal_router.post('/tex-pdf/')
@inject
async def send_documents(
    payload: SendDocumentsRequest,
    bot: Annotated[Bot, Depends()],
):
    await bot.send_chat_action(chat_id=payload.telegram_id, action='upload_document')
    await asyncio.sleep(1.0)
    tex_file = FSInputFile(path=payload.filename + '.tex', filename='resume.tex')
    await bot.send_document(chat_id=payload.telegram_id, document=tex_file)
    Path(payload.filename + '.tex').unlink(missing_ok=True)
    await bot.send_chat_action(chat_id=payload.telegram_id, action='upload_document')
    await asyncio.sleep(1.0)
    pdf_file = FSInputFile(path=payload.filename + '.pdf', filename='resume.pdf')
    await bot.send_document(chat_id=payload.telegram_id, document=pdf_file)
    Path(payload.filename + '.pdf').unlink(missing_ok=True)
    return JSONResponse(content={'ok': True}, status_code=status.HTTP_200_OK)
