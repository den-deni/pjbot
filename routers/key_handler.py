import asyncio

from aiogram import Router, F, html
from  aiogram.types import CallbackQuery

from utils.encoder import Encoder
from database.model import Database



key_router = Router()
en = Encoder()
db = Database()


@key_router.callback_query(F.data.in_(["key_create", "key_change", "key_delete", "key_show"]))
async def key_manager(call: CallbackQuery):
    action = call.data
    user_id = call.from_user.id
    check_key = await db.get_key(user_id)
    key = en.genkey()
    if action == "key_create":
        if not check_key:
            await db.set_key(user_id, key)
            await call.answer(text="You key create and save", show_alert=True)
        else:
            await call.answer(f"You have key, can change", show_alert=True)
    if action == "key_change":
        if check_key:
            await db.update_key(user_id, key)
            await call.answer(text="You key update", show_alert=True)
        else:
            await call.answer(text="You not have key, can create", show_alert=True)
    if action == "key_delete":
        if check_key:
            await db.delete_key(user_id)
            await call.answer(text="You key delete, can create", show_alert=True)
        else:
            await call.answer(text="You not have key", show_alert=True)
    if action == "key_show":
        if not check_key:
            await call.answer(text="Not key", show_alert=True)
        else:
            key = await db.get_key(user_id)
            msg = await call.message.answer(text=f"{html.spoiler(key)}")
            await call.answer(text="Copy and save, delete 10s", show_alert=True)
            await asyncio.sleep(10)
            await msg.delete()
