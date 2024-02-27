from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message

greeting_router = Router()


@greeting_router.message(CommandStart())
async def start(message: Message):
    text = 'Hello there.'
    text += '\nType /auth to authenticate, type /resume after that to choose and transform resume'
    await message.answer(text)
