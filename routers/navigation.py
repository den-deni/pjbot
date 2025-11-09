from aiogram import Router, F, html, Bot
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.filters import CommandStart


from keyboard.inlain_kb import kb_builder, get_settings
from database.model import Database




select_router = Router()
db = Database()


menu_button = kb_builder(["Encoder", "Settings"],
                         ["encoder", "settings"],
                         size=2)



with_key_btn = kb_builder(["Encoder", "Settings", "Key", "Encoder_File"],
                          ["encoder", "settings", "key", "encoder_file"],
                          size=1)



@select_router.message(CommandStart())
async def start_bot(message: Message):
    user_id = message.from_user.id
    name = message.from_user.full_name

    user = await db.user_exists(user_id)
    if not user:
        await db.create_user(user_id, name)

    status = await db.get_status(user_id)
    if status:
        kb = with_key_btn
        text = f"{html.italic('You anonim status off')}"
    else:
        kb = menu_button
        text = f"Hello {html.bold(name)}! I`m Encoder bot\n{html.italic('You status anonim')}"
    pic = FSInputFile("media/bot_imj.jpg")
    await message.bot.send_photo(chat_id=user_id,
                         photo=pic,
                         caption=f"{text}",
                         reply_markup=kb)





@select_router.callback_query(F.data == "encoder")
async def choice_method(call: CallbackQuery, bot: Bot):
    await bot.edit_message_caption(chat_id=call.from_user.id,
                                   message_id=call.message.message_id,
                                   caption=f"{html.italic("Make a choice")}",
                                   reply_markup=kb_builder(text=["Encrypt", "Decrypt", "Back"],
                                                           callback=["encrypt", "decrypt", "back"],
                                                           size=2))




@select_router.callback_query(F.data == "encoder_file")
async def choise_method_for_file(call: CallbackQuery, bot: Bot):
    await bot.edit_message_caption(chat_id=call.from_user.id,
                                   message_id=call.message.message_id,
                                   caption=f"{html.italic('You can crypt file')}",
                                   reply_markup=kb_builder(["F_encrypt", "F_decrypt", "Back"],
                                                           ["fencrypt", "fdecrypt", "back"],
                                                           size=2))
    



@select_router.callback_query(F.data == "back")
async def back_button(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    status = await db.get_status(user_id)
    if status:
        kb = with_key_btn
    else:
        kb = menu_button
    await bot.edit_message_caption(chat_id=user_id,
                                   message_id=call.message.message_id,
                                   caption=f"{html.italic("Main menu")}",
                                   reply_markup=kb)
    
    


@select_router.callback_query(F.data == "settings")
async def settings_button(call: CallbackQuery):
    user_id = call.from_user.id

    status = await db.get_status(user_id)
    btn = get_settings(status)
    
    await call.bot.edit_message_caption(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        caption=f"{html.italic('Status options')}",
        reply_markup=btn
    )




@select_router.callback_query(F.data == "key")
async def key_menu(call: CallbackQuery):
    await call.bot.edit_message_caption(chat_id=call.from_user.id,
                                        message_id=call.message.message_id,
                                        caption=f"{html.italic('You can change settings key')}",
                                        reply_markup=kb_builder(
                                                                ["CreateKey", "ChangeKey", "DeletKey", "ShowKey", "Back"],
                                                                ["key_create", "key_change", "key_delete", "key_show", "back"],
                                                                size=2))
    await call.answer()
