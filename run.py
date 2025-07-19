import asyncio
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher

from app.user import user_router
from app.admin import admin_router


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN_TBOT'))
    dp = Dispatcher()

    dp.include_router(user_router)
    dp.include_router(admin_router)

    await dp.start_polling(bot)





if __name__ == '__main__':
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        pass