from aiogram import BaseMiddleware
from utils.encoder import Encoder


class EncoderMiddleweare(BaseMiddleware):
    async def __call__(self, handler, event, data):
        data["encoder"] = Encoder()
        return await handler(event, data)
    