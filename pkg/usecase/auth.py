from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded
import os

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")



async def number(phone_number):
    app = Client(f"{phone_number}", API_ID, API_HASH)

    try:   
        if await app.connect():
            # asyncio.create_task(start_process())
            pass
        else:


            resp = await app.send_code(phone_number)

            print(f"Код отправлен на номер {phone_number}, hash = {resp.phone_code_hash}")
            return resp.phone_code_hash,app
        
    except Exception as e:
        return e
    
async def authorize_in_pyrogram(phone,code,hash,app:Client):
    appe = Client(f"{phone}", API_ID, API_HASH)
    try:
        if await appe.connect():
            print("pass")
            pass
        else:
            print(f"Авторизован {code} {phone} {hash}")

            await appe.sign_in(phone_number=phone, phone_code=code,phone_code_hash=hash)
            return None
    except SessionPasswordNeeded:
        return "Auth2"
    except Exception as e:
        return e   
    
async def password(password,phone_number):
    app = Client(f"{phone_number}", API_ID, API_HASH)
    try:
        if await app.connect():
            pass
        else:
            await app.check_password(password)
            print(f"Пароль {password}")

            return None
    except Exception as e:
        return e