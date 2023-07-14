from database import initialize_database
from middlewares import setup


async def on_startup(dispatcher):
    setup(dispatcher)
    await initialize_database()


if __name__ == "__main__":
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
