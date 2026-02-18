import asyncio
import os
from pathlib import Path

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext


from middleware.middleweare import EncoderMiddleweare
from utils.encoder import Encoder
from database.model import Database
from state.botstate import BotState



file_router = Router()
db = Database()


file_router.message.middleware(EncoderMiddleweare())

@file_router.callback_query(F.data.in_(["fencrypt", "fdecrypt"]))
async def start_process_for_file(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    check_key = await db.get_key(user_id)
    if check_key:
        await state.update_data(action=call.data, key=check_key)
        await call.answer(text="Ok send me file max size must be 20MB", show_alert=True)
        await state.set_state(BotState.file_data)
    else:
        await call.answer(text="You not have key", show_alert=True)





@file_router.message(BotState.file_data)
async def process_for_file(message: Message, state: FSMContext, encoder: Encoder):
    data = await state.get_data()
    action = data.get("action")
    key = data.get("key")

    file_id = None
    file_name = None
    file_size = None

    # 🔹 Визначаємо тип файлу
    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name
        file_size = message.document.file_size
    elif message.audio:
        file_id = message.audio.file_id
        file_name = message.audio.file_name or "audio.mp3"
        file_size = message.audio.file_size
    elif message.voice:
        file_id = message.voice.file_id
        file_name = "voice.ogg"
        file_size = message.voice.file_size
    else:
        if message.photo:
            await message.delete()
            msg = await message.answer("⚠️ Format must be a document, audio or voice file.")
            await asyncio.sleep(10)
            await msg.delete()
        return

    # 🔸 Обмеження на розмір
    MAX_FILE_SIZE = 20 * 1024 * 1024
    if file_size > MAX_FILE_SIZE:
        await message.answer("⚠️ File > 20MB")
        await asyncio.sleep(10)
        await message.delete()
        return

    # 🔸 Завантажуємо файл
    file_info = await message.bot.get_file(file_id)
    os.makedirs("downloads", exist_ok=True)
    file_path = f"downloads/{file_name}"

    await message.bot.download_file(file_info.file_path, destination=file_path)
    await message.delete()
    msg = await message.answer(text="Wait in process...⏳")
    await asyncio.sleep(25)
    await msg.delete()

    # 🔸 Шифрування або розшифрування
    if action == "fencrypt":
        result_path = encoder.encrypt_file(file_path, key)
        caption = "🔒File encrypt(auto delete 60с)"
    else:
        result_path = encoder.decrypt_file(file_path, key)
        caption = "🔓File decrypt(auto delete 60с)"

    # 🔸 Надсилаємо результат
    msg = await message.answer_document(FSInputFile(result_path), caption=caption)
    await asyncio.sleep(60)
    await msg.delete()

    # 🔸 Очищаємо тимчасові файли
    await state.clear()
    Path(file_path).unlink(missing_ok=True)
    Path(result_path).unlink(missing_ok=True)







    

    