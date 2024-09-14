from aiogram import Router
import sys,os, uuid
import asyncio
from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.utils import ainput
# from pkg.usecase. import start_process
from pkg.usecase.states import States
from pkg.repository.redis import RD
r = Router()

API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)

@r.message(F.text == "/start")
async def start(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Привет!")
    loop = asyncio.get_event_loop()
    # telegram_logger = TelegramLogger(bot, msg.chat.id, loop)
    # sys.stdout = telegram_logger

    await msg.answer("Перешли сообщение того с кем хочешь поставить аву")

    await state.set_state(States.forward)

@r.message(States.forward)
async def get_forward(msg: Message, state: FSMContext):
    if msg.forward_from:
        try:
            user_id = msg.forward_from.id
            token = uuid.uuid4()
            RD.client.lpush("tokens", "123")
            await bot.send_message(user_id,"Вас пригласили")
            
        except Exception:
            await msg.answer("Попросите этого пользователя начать работу с ботом и попробуйте еще раз")
    
    await state.update_data(user_id=user_id)
    await state.set_state(States.number)

# @r.message(States.number)
# async def handle_phone_number(msg: Message, state: FSMContext):
#     phone_or_token = msg.text

#     await state.update_data(phone_or_token=phone_or_token)

#     asyncio.create_task(authorize_in_pyrogram(phone_or_token))