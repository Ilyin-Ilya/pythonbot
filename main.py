import asyncio
from errno import errorcode
import mysql.connector
import asyncpg
import sys
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN
from config import USER, HOST, password, database

try:
    cnx = mysql.connector.connect(user=USER, password=password,
                              host=HOST,
                              database=database)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
    sys.exit()
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
    sys.exit()
  else:
    print(err)
    sys.exit()


# loop = asyncio.get_event_loop()
# Поток нам не нужен, т.к. он и так создается в диспатчере.
bot = Bot(BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()

dp = Dispatcher(bot,storage=storage)

async def on_shutdown(dp):
    await bot.close()
    await storage.close()
    await cnx.close()

if __name__ == '__main__':
    from handlers import dp

    executor.start_polling(dp,on_shutdown=on_shutdown)