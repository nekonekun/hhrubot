from typing import Annotated

from aiogram import Router, flags, F
from aiogram.filters import Command
from aiogram.types import Message, WebAppInfo, Chat
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from dishka.integrations.aiogram import inject, Depends

from hhrubot.application.headhunter import BuildLoginURL, GetResumeList


resume_router = Router()


@resume_router.message(Command(commands=['auth']), F.chat.type == 'private')
@inject
async def auth_user(
    message: Message,
    *,
    build_login_url: Annotated[BuildLoginURL, Depends()],
):
    builder = InlineKeyboardBuilder()
    login_url = build_login_url(telegram_id=message.from_user.id)
    builder.add(InlineKeyboardButton(text='Sign in', web_app=WebAppInfo(url=login_url)))
    await message.answer(
        'Click button below to open hh.ru login page',
        reply_markup=builder.as_markup()
    )


@resume_router.message(Command(commands=['resume']), F.chat.type == 'private')
@flags.employee
@inject
async def show_resumes(
    message: Message,
    *,
    get_resume_list: Annotated[GetResumeList, Depends()],
):
    resumes = await get_resume_list()
    resumes = ', '.join(resume['title'] for resume in resumes['items'])
    await message.answer(f'Here are your resumes:\n{resumes}')
