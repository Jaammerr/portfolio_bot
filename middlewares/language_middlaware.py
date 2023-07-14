from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.middlewares import BaseMiddleware
from database import Users


class LanguageMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    @staticmethod
    async def on_pre_process_message(message: types.Message, data: FSMContext):
        user_id = message.from_user.id
        language = await Users().get_user_language(user_id)
        await data.update_data(language=language)

    @staticmethod
    async def on_pre_process_callback_query(query: types.CallbackQuery, data: FSMContext):
        user_id = query.from_user.id
        language = await Users().get_user_language(user_id)
        await data.update_data(language=language)
