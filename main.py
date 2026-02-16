import asyncio
# import logging
# import sys

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from routers.main_pouter import routers
from commands.list_cmd import private
from database.model import Database
from config.config import Config


# Bot token can be obtained via https://t.me/BotFather
TOKEN = Config.token



dp = Dispatcher()
db = Database()




async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(*routers)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await bot.delete_webhook(drop_pending_updates=True)

    await db.create_table()


    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())