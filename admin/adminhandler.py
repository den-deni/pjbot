from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command


from database.model import Database
from middleware.middleweare import AdminF


admin_router = Router()
db = Database()


admin_router.message.middleware(AdminF())

@admin_router.message(Command("list"))
async def get_users(message: Message):
    users = await db.get_all_users()
    text_lines = ["User id | Username"]
    for tg_id, username in users:
        text_lines.append(f"{tg_id} | {username}")


    file_path = "users.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(text_lines))

    answer_doc = FSInputFile(file_path)
    await message.answer_document(
            document=answer_doc,
            caption="Users Encoder"
        )

        