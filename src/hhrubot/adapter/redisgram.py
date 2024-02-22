from typing import Any

from aiogram.fsm.storage.redis import RedisStorage, StorageKey


class RedisGram:
    def __init__(self, storage: RedisStorage, bot_id: int):
        self.storage = storage
        self.bot_id = bot_id

    async def update_data(self, *, data: dict[str, Any], user_id: int, chat_id: int | None = None):
        if not chat_id:
            chat_id = user_id
        key = StorageKey(bot_id=self.bot_id, chat_id=chat_id, user_id=user_id)
        context_data = await self.storage.get_data(key)
        context_data.update(data)
        await self.storage.set_data(key=key, data=context_data)
