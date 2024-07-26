import asyncio
import logging
from aiogram import Bot, Dispatcher
from private import TOKEN
from handlers import nutri


logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dp = Dispatcher()
dp.include_routers(nutri.router)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


