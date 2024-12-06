import asyncio, logging
from aiogram import Bot, Dispatcher, Router, F
from pkg.handlers.router import dp
from pkg.handlers.handler import r
import os

bot = Bot(token=os.getenv("API_TOKEN"))

async def main():
    logging.basicConfig(level=logging.INFO)

    dp.include_router(r)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())