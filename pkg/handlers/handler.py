from aiogram import Router
import sys,os, uuid
import asyncio
from aiogram import Bot, Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded
from pkg.usecase.kb import menu
# from pkg.usecase. import start_process
from pkg.usecase.states import States
from pkg.repository.redis import RD
r = Router()

API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)

@r.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    await state.clear()
    if msg.text.startswith("/start invite_"):
        _,token = msg.text.split('_')
        print(token)
        user_id = RD.client.get(token)
        await msg.answer(text=f"Вас пригласил {user_id}, дождитесь пока ваш партнер запустит процесс")
        await bot.send_message(user_id, "Ваш партнер присоединился", reply_markup=menu(user_id))
        RD.client.set(user_id,msg.from_user.id)
    else:
        await msg.answer("Привет!")

        # telegram_logger = TelegramLogger(bot, msg.chat.id, loop)
        # sys.stdout = telegram_logger

        token = uuid.uuid4()
        link = f"https://t.me/ChinaMapp_Queue_bot?start=invite_{str(token)}"
        await msg.answer(f"Скинь этот инвайт линк партнеру\n{link}")
        RD.client.set(str(token), msg.from_user.id)

@r.callback_query(F.data.startswith("start_"))
async def begin(cb:CallbackQuery, state:FSMContext):
    _, user_id = cb.data.split("_")

    partner_id = RD.client.get(user_id)
    

    await bot.send_message(partner_id, "Ваш партнер начал процесс")

    await bot.send_message(user_id, "Введите ваш номер телефона привязанный к тг")
    await bot.send_message(partner_id, "Введите ваш номер телефона привязанный к тг")

    await state.update_data(user_id=user_id,partner_id=partner_id)
    await state.set_state(States.number)

@r




# @r.message(States.forward)
# async def get_forward(msg: Message, state: FSMContext):
#     if msg.forward_from:
#         try:
#             user_id = msg.forward_from.id
#             token = uuid.uuid4()
#             RD.client.set(str(token), msg.from_user.id)
#             await bot.send_message(user_id,"Вас пригласили")
            
#         except Exception:
#             await msg.answer("Попросите этого пользователя начать работу с ботом и попробуйте еще раз")
    
#     await state.update_data(user_id=user_id)
#     await state.set_state(States.number)

# @r.message(States.number)
# async def handle_phone_number(msg: Message, state: FSMContext):
#     phone_or_token = msg.text

#     await state.update_data(phone_or_token=phone_or_token)

#     asyncio.create_task(authorize_in_pyrogram(phone_or_token))