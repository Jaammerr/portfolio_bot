from aiogram import types
from aiogram.dispatcher import FSMContext

from database import Users
from loader import dp, bot
from states import *
from keyboards import *
from handlers.users.start import send_start_message
from utils import check_state_for_delete_message


@dp.callback_query_handler(text="cancel_action", state="*")
async def cancel_action(jam: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()

    if current_state in AddNewProjectStates.states_names:
        await jam.message.edit_text(
            "📃  <b>Проекты:</b>", reply_markup=get_admin_projects_menu()
        )
        await MenuManagerStates.activate_projects.set()

    elif current_state in ShowProjectsStates.states_names:
        if current_state == ShowProjectsStates.admin_delete_project.state:
            await jam.message.edit_text(
                "📃  <b>Проекты:</b>", reply_markup=get_admin_projects_menu()
            )
            await MenuManagerStates.activate_projects.set()

        elif current_state == ShowProjectsStates.show_project_details_for_user.state:
            language = await Users().get_user_language(jam.from_user.id)
            state_data = await state.get_data()
            messages_to_delete = state_data["messages_to_delete"]

            with open("./image1.jpg", "rb") as photo:
                if 'page' in await state.get_data():
                    projects_kb = await get_projects_menu(page=(await state.get_data())['page'], language=language)
                else:
                    projects_kb = await get_projects_menu(language=language)

                message = await bot.send_photo(
                    chat_id=jam.from_user.id, photo=photo, reply_markup=projects_kb, caption=localization.get_translation('select_project_text', language=language)
                )
                for message_to_delete in messages_to_delete:
                    await message_to_delete.delete()

                await state.update_data(start_message=message)

            await ShowProjectsStates.show_projects_for_user.set()

        elif current_state == ShowProjectsStates.show_projects_for_user.state:
            await send_start_message(jam.message.chat.id, state)
            await check_state_for_delete_message(state)

    elif (
        current_state in MenuManagerStates.states_names
        or current_state in BroadcasterStates.states_names
    ):
        await jam.message.edit_text(
            "💎  <b>Админ-панель:</b>", reply_markup=get_admin_menu()
        )
        await state.finish()

    else:
        if not await check_state_for_delete_message(state):
            await send_start_message(jam.message.chat.id, state)
