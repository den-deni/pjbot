from aiogram import BaseMiddleware
from utils.encoder import Encoder
from typing import Any, Awaitable, Callable, Dict
from aiogram.types import Message, TelegramObject

from config.config import config


class EncoderMiddleweare(BaseMiddleware):
    async def __call__(self, handler, event, data):
        data["encoder"] = Encoder()
        return await handler(event, data)
    


class AdminF(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]):
        if event.from_user.id != config.admin_id:
            return
        return await handler(event, data)

