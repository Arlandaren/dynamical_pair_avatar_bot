import asyncio, logging
from aiogram import Bot, Dispatcher, Router, F
from pkg.handlers.router import r

API_TOKEN = '7428911519:AAGJTtCFV6by3tRMQG7VgGD4-FJtCtFnVps'

bot = Bot(token=API_TOKEN)

async def main():
    logging.basicConfig(level=logging.INFO)
    p = Dispatcher()
    p.include_router(r)

    await p.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())