import asyncio

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


from database.model import Database
from middleware.middleweare import AdminF


admin_router = Router()
db = Database()


admin_router.message.middleware(AdminF())

@admin_router.message(Command("list"))
async def get_users(message: Message):
    await message.delete()
    users = await db.get_all_users()
    text = "\n".join(
        f"{user["id"]} | {user["username"]}"
        for user in users
    )
    msg = await message.answer(text)
    await asyncio.sleep(30)
    await msg.delete()


        