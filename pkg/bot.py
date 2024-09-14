# import sys
# import io
# import asyncio
# from aiogram import Bot, Dispatcher, Router, F
# from aiogram.types import Message
# from concurrent.futures import ThreadPoolExecutor
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from usecase import start_process

# API_TOKEN = '7428911519:AAGJTtCFV6by3tRMQG7VgGD4-FJtCtFnVps'

# bot = Bot(token=API_TOKEN)

# class States(StatesGroup):
#     number = State()

# class TelegramLogger(io.StringIO):
#     def __init__(self, bot, chat_id, loop):
#         super().__init__()
#         self.bot = bot
#         self.chat_id = chat_id
#         self.loop = loop
#         self.executor = ThreadPoolExecutor()

#     def write(self, message):
#         super().write(message)
#         if message.strip():
#             asyncio.run_coroutine_threadsafe(self.bot.send_message(self.chat_id, message), self.loop)

#     def flush(self):
#         super().flush()

# r = Router()

# @r.message(F.text == "/start")
# async def start(msg: Message, state:FSMContext):
#     await msg.answer(text="Привет")
#     loop = asyncio.get_event_loop()
#     telegram_logger = TelegramLogger(bot, msg.chat.id, loop)
#     sys.stdout = telegram_logger

#     asyncio.create_task(start_process())

#     await state.set_state(States.number)


# @r.message(States.number)
# async def handle_number(msg: Message):
#     print(msg.text)

# async def main():
#     loop = asyncio.get_event_loop()
#     p = Dispatcher()
#     p.include_router(r)

#     await p.start_polling(bot, loop=loop)

# if __name__ == "__main__":
#     asyncio.run(main())


import sys,os
import io
import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from concurrent.futures import ThreadPoolExecutor
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.utils import ainput
from usecase import start_process

API_TOKEN = os.getenv("API_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_TOKEN")


bot = Bot(token=API_TOKEN)

class States(StatesGroup):
    forward = State()
    number = State()
    password = State()
    code = State()

class TelegramLogger(io.StringIO):
    def __init__(self, bot, chat_id, loop):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id
        self.loop = loop
        self.executor = ThreadPoolExecutor()

    def write(self, message):
        super().write(message)
        if message.strip():
            asyncio.run_coroutine_threadsafe(self.bot.send_message(self.chat_id, message), self.loop)

    def flush(self):
        super().flush()

r = Router()

@r.message(F.text == "/start")
async def start(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Привет!")
    loop = asyncio.get_event_loop()
    telegram_logger = TelegramLogger(bot, msg.chat.id, loop)
    sys.stdout = telegram_logger

    await msg.answer("Перешли сообщение того с кем хочешь поставить аву")

    await state.set_state(States.forward)

@r.message(States.forward)
async def get_forward(msg: Message, state: FSMContext):
    if msg.forward_from:
        try:
            user_id = msg.forward_from.id
            await bot.send_message(user_id,"Вас пригласили")
            
        except Exception:
            await msg.answer("Попросите этого пользователя начать работу с ботом и попробуйте еще раз")
    
    await state.update_data(user_id=user_id)
    await state.set_state(States.number)

@r.message(States.number)
async def handle_phone_number(msg: Message, state: FSMContext):
    phone_or_token = msg.text

    await state.update_data(phone_or_token=phone_or_token)

    asyncio.create_task(authorize_in_pyrogram(phone_or_token))

async def authorize_in_pyrogram(phone_number):
    app = Client("my_account", API_ID, API_HASH)
    print("Asdasdasd")

        
    if await app.connect():
        asyncio.create_task(start_process())
    else:
        print(f"Код отправлен на номер {phone_number}")

        print("Введите код")
        await app.send_code("89145045696")


# @r.message(States.code)
# async def code(msg:Message, state: FSMContext):
#     code = msg.text

    


async def main():
    # loop = asyncio.get_event_loop()
    p = Dispatcher()
    p.include_router(r)

    await p.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
