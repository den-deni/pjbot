from aiogram import BaseMiddleware
from utils.encoder import Encoder
from aiogram.types import TelegramObject

import aiosqlite

DB_PATH = "data.db"

class DBMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with aiosqlite.connect(DB_PATH) as db:
            data["db"] = db
            return await handler(event, data)



class EncoderMiddleweare(BaseMiddleware):
    async def __call__(self, handler, event, data):
        data["encoder"] = Encoder()
        return await handler(event, data)
    