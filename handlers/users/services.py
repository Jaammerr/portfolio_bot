from aiogram import types
from aiogram.dispatcher import FSMContext

from database import Users
from keyboards import get_cancel_action_kb
from loader import dp, localization


@dp.callback_query_handler(text="user_show_services", state="*")
async def user_show_services(jam: types.CallbackQuery, state: FSMContext):
    start_message = (await state.get_data()).get("start_message")
    language = await Users().get_user_language(jam.from_user.id)

    await start_message.edit_caption(
        caption=localization.get_translation("services_text", language=language),
        reply_markup=get_cancel_action_kb(language=language)
    )
