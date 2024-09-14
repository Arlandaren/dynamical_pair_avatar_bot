import io
import asyncio
from concurrent.futures import ThreadPoolExecutor

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