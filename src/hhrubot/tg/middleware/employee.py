from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware, Bot
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject

from hhrubot.adapter.headhunter import HeadhunterAccessToken


class EmployeeMiddleware(BaseMiddleware):
    """Mix hh.ru access token into dishka context data"""
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ):
        is_employee_method = get_flag(data, 'employee')
        if is_employee_method:
            state = data['state']
            context_data = await state.get_data()
            access_token = context_data.get('access_token')
            if not access_token:
                bot: Bot = data['bot']
                text = 'Sorry, but you need to authenticate '
                text += 'before using this command'
                await bot.send_message(
                    chat_id=event.chat.id,
                    text=text,
                )
                return None
            data['dishka_container'].context.update(
                {HeadhunterAccessToken: access_token},
            )
        return await handler(event, data)
