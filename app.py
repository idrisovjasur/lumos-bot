import asyncio
import logging
import sys

from loader import dp, bot, db
from handlers.users.start import start_router
from handlers.users.main import main_router
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def main() -> None:
    dp.include_router(start_router)
    dp.include_router(main_router)
    await set_default_commands()
    await on_startup_notify()
    try:
        await db.create()
        # await db.create_table_users()
    except Exception as e:
        print(e)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())