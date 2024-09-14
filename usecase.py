import asyncio, requests,json,aiohttp
from pyrogram import Client
from io import BytesIO
import os


API_TOKEN = os.getenv("API_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_TOKEN")

api_id2 = '27808347'
api_hash2 = '0ceea5770b7fedf15f4e76f3aabeca6c'
phone_number2 = '89145045696'

# def get_photo(url:str):
#     resp = requests.get(url.strip())

#     return BytesIO(resp.content)

async def get_photo(url_list: str):
    imgs_list = []
    async with aiohttp.ClientSession() as session:
        for url in url_list:
            async with session.get(url.strip()) as resp:
                if resp.status != 200:
                    print(f"Error fetching image from {url}, status code: {resp.status}")
                    return None
                else:
                    image_bytes = await resp.read()
                    imgs_list.append(BytesIO(image_bytes))
        return {
        "left": imgs_list[0],
        "right": imgs_list[1]}           

async def start_process():
    imgs_orig = []
    imgs_work = []
    with open("imgs.json", "r", encoding="utf-8") as f:
        imgs:dict = json.load(f)
    for i in imgs.keys():
        imgs_orig.append([imgs[i]["left"], imgs[i]["right"]])

    # async with Client("my_account", api_id1, api_hash1) as app1, Client("my_account_2", api_id2, api_hash2) as app2:
    #     while True:
    #         if imgs_work == []:
    #             imgs_work = imgs_orig
    #         url_list = imgs_work.pop()

    #         print(f"Setting profile {url_list}")

    #         photos = await get_photo(url_list)

    #         if photos:
    #             await app1.set_profile_photo(photo=photos["left"])
    #             await app2.set_profile_photo(photo=photos["right"])
    #         else:
    #             print("err")

    #         await asyncio.sleep(5)
    async with Client("my_account", api_id1, api_hash1) as app:
        while True:
            if imgs_work == []:
                imgs_work = imgs_orig
            url_list = imgs_work.pop()

            print(f"Setting profile {url_list}")

            photos = await get_photo(url_list)

            if photos:
                await app.set_profile_photo(photo=photos["right"])
            else:
                print("err")

            await asyncio.sleep(5)

if __name__ == "__main__":
    print("Starting...")

    asyncio.run(start_process())
