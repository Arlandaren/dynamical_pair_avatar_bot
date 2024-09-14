from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded
import os

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_TOKEN")



async def auth():
    app = Client("my_account", API_ID, API_HASH)
    print("Asdasdasd")

        
    if await app.connect():
        # asyncio.create_task(start_process())
        pass
    else:
        print(f"Код отправлен на номер {phone_number}")

        print("Введите код")
        await app.send_code("89145045696")