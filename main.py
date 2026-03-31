import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import load_config
from handlers.start import router as start_router
from handlers.catalog import router as catalog_router
from handlers.order import router as order_router


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    config = load_config()
    bot = Bot(token=config.bot_token)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(catalog_router)
    dp.include_router(order_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
