from aiogram import Router, F, html
from aiogram.types import CallbackQuery


from database.model import Database
from keyboard.inlain_kb import get_settings



settings_router = Router()
db = Database()




@settings_router.callback_query(F.data.startswith("toggle_settings"))
async def change_settings(call: CallbackQuery):
    user_id = call.from_user.id

    # Отримуємо поточний статус
    current_status = await db.get_status(user_id)
    if current_status is None:
        current_status = False  # якщо користувача ще нема або поле порожнє

    # Міняємо стан
    new_status = not current_status

    # Зберігаємо в БД
    await db.set_status(user_id, new_status)

    if new_status == True:
        text = f"{html.italic('Anonim off')}"
    else:
        text = f"{html.italic('Anonim on')}"

    # Оновлюємо клавіатуру
    await call.bot.edit_message_caption(
        chat_id=user_id,
        message_id=call.message.message_id,
        caption=f"{text}",
        reply_markup=get_settings(new_status)
    )
    await call.answer()

