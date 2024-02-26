from typing import Annotated

from aiogram import F, Router, flags
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from dishka.integrations.aiogram import Depends, inject

from hhrubot.application.headhunter import (
    BuildLoginURL,
    GetResume,
    GetResumeList,
)
from hhrubot.queue.tex import make_documents
from hhrubot.tg.callback.resume import ResumeData

resume_router = Router()


@resume_router.message(Command(commands=['auth']), F.chat.type == 'private')
@inject
async def auth_user(
    message: Message,
    state: FSMContext,
    *,
    build_login_url: Annotated[BuildLoginURL, Depends()],
):
    context_data = await state.get_data()
    access_token = context_data.get('access_token')
    if access_token:
        text = 'You are already authenticated.\n'
        text += 'Click button below if you want to sign in as another user.'
    else:
        text = 'Click button below to open hh.ru login page'
    builder = InlineKeyboardBuilder()
    login_url = build_login_url(telegram_id=message.from_user.id)
    builder.add(
        InlineKeyboardButton(
            text='Sign in',
            web_app=WebAppInfo(url=login_url),
        ),
    )
    await message.answer(text, reply_markup=builder.as_markup())


@resume_router.message(Command(commands=['resume']), F.chat.type == 'private')
@flags.employee
@inject
async def show_resumes(
    message: Message,
    *,
    get_resume_list: Annotated[GetResumeList, Depends()],
):
    resumes = await get_resume_list()
    builder = InlineKeyboardBuilder()
    for resume in resumes.items:
        builder.row(
            InlineKeyboardButton(
                text=resume.title,
                callback_data=ResumeData(resume_id=resume.id).pack()),
        )
    await message.answer(
        'Here are your resumes. Click one to process',
        reply_markup=builder.as_markup(),
    )


@resume_router.callback_query(ResumeData.filter())
@flags.employee
@inject
async def process_resume(
    callback_query: CallbackQuery,
    callback_data: ResumeData,
    *,
    get_resume: Annotated[GetResume, Depends()],
):
    await callback_query.answer()
    await callback_query.message.delete_reply_markup()
    text = 'It will take some time (around 1-2 minutes) to generate files.'
    text += ' Please, be patient.'
    await callback_query.message.answer(text)
    resume = await get_resume(callback_data.resume_id)
    text = callback_query.message.text + '\n\n' + resume.title
    await callback_query.message.edit_text(text)
    make_documents.send(
        telegram_id=callback_query.from_user.id,
        filename=callback_data.resume_id,
        resume=resume.model_dump(),
    )
