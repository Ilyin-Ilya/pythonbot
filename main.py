import asyncio

from aiogram import Bot, Dispatcher, executor
from config import BOT_TOKEN

# loop = asyncio.get_event_loop()
# Поток нам не нужен, т.к. он и так создается в диспатчере.
bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

if __name__ == '__main__':
    from handlers import dp

    executor.start_polling(dp)