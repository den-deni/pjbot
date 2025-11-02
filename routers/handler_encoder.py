import asyncio
import base64
import ast

from aiogram import Router, F, html
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from utils.encoder import Encoder
from state.botstate import BotState
from middleware.middleweare import EncoderMiddleweare
from database.model import Database
from keyboard.inlain_kb import about_button


encoder_router = Router()
db = Database()



encoder_router.callback_query.middleware(EncoderMiddleweare())
encoder_router.message.middleware(EncoderMiddleweare())

@encoder_router.message(Command("key"))
async def gen_key(message: Message, encoder: Encoder):
    key = encoder.genkey()
    await message.delete()

    msg1 = await message.answer(text=f"{html.italic('Save key, dellete 10s')}")
    msg2 = await message.answer(text=f"{html.spoiler(key)}")

    await asyncio.sleep(10)
    for msg in [msg1, msg2]:
        try:
            await msg.delete()
        except:
            pass
    


    

@encoder_router.callback_query(F.data.in_(["encrypt", "decrypt"]))
async def select_encrypt(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    check_status = await db.get_status(user_id)
    if check_status:
        key = await db.get_key(user_id)
        await state.update_data(action=call.data, key=key)
        await call.answer(text=f"Send me text", show_alert=True)
        await state.set_state(BotState.user_data)
    else:
        await state.update_data(action=call.data)
        await state.set_state(BotState.key)
        await call.answer("Ok send me key", show_alert=True)



@encoder_router.message(BotState.key)
async def next_state(message: Message, state: FSMContext):
    raw_key = message.text.strip()

    # ✅ Перевірка формату b'...'
    try:
        # Безпечно перетворюємо текст в об’єкт Python (наприклад, b'...' → bytes)
        key = ast.literal_eval(raw_key)

        # Переконаємось, що це дійсно bytes
        if not isinstance(key, (bytes, bytearray)):
            raise ValueError("Ключ має бути у форматі байтів")

        # Перевіримо, що ключ валідний для Fernet (base64 з 32 байт)
        decoded = base64.urlsafe_b64decode(key)
        if len(decoded) != 32:
            raise ValueError("Довжина ключа некоректна")
    except Exception:
        await message.answer(text=f"{html.italic("Invalid key!!!")}")
        await message.delete()
        return


    await state.update_data(key=key)
    msgt = await message.answer("Ok send me text")
    await state.set_state(BotState.user_data)
    await asyncio.sleep(5)
    await msgt.delete()

    try:
        await message.delete()
    except Exception:
        pass


@encoder_router.message(BotState.user_data, F.text)
async def finish_state(message: Message, state: FSMContext, encoder: Encoder):
    await state.update_data(userdata=message.text)
    data = await state.get_data()
    key = data['key']
    userdata = data['userdata']
    action = data['action']

    if not key:
        await message.answer(text=f"You not have key")
        return

    if action == 'encrypt':
        answer_text = encoder.encrypt(text=userdata, key=key)
    else:
        answer_text = encoder.decrypt(encrypted_text=userdata, key=key)
    
    try:
        await message.delete()
    except Exception:
        pass

    try:
        msg = await message.bot.send_message(chat_id=message.from_user.id, text=answer_text)
        await asyncio.sleep(30)
        await msg.delete()
    except Exception:
        await message.answer(f"{html.italic('Sorry I can not send')}")
    
    await state.clear()
   



@encoder_router.message(Command("about"))
async def get_about_button(message: Message):
    await message.delete()
    await message.answer(text="Instruction bot", reply_markup=about_button)
