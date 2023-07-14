from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards import get_admin_projects_menu, get_users_menu, get_admin_broadcaster_kb
from loader import dp
from states import MenuManagerStates
from handlers.users.start import send_start_message


@dp.callback_query_handler(
    text=[
        "admin_projects",
        "admin_users",
        "admin_broadcast",
        "admin_switch_to_user_menu",
    ],
    state="*",
)
async def admin_menu_manager(jam: types.CallbackQuery, state: FSMContext):
    if jam.data == "admin_projects":
        await MenuManagerStates.activate_projects.set()
        await jam.message.edit_text(
            "📃  <b>Проекты:</b>", reply_markup=get_admin_projects_menu()
        )

    elif jam.data == "admin_users":
        await MenuManagerStates.activate_users.set()

    elif jam.data == "admin_broadcast":
        await jam.message.edit_text(
            "📢  <b>Выберите тип рассылки: </b>", reply_markup=get_admin_broadcaster_kb()
        )
        await MenuManagerStates.activate_broadcaster.set()

    else:
        await state.finish()
        await jam.message.delete()
        await send_start_message(jam.message.chat.id, state)
