from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified

from loader import dp, bot, localization
from keyboards import get_projects_menu, get_cancel_action_kb, get_admin_projects_menu
from states import ShowProjectsStates, MenuManagerStates
from database import Projects, Users
from utils import translate_text


@dp.callback_query_handler(
    lambda jam: jam.data.startswith("page_projects_prev")
    or jam.data.startswith("page_projects_next"),
    state=[
        ShowProjectsStates.show_projects_for_user,
        ShowProjectsStates.admin_delete_project,
    ],
)
async def swap_page(
    jam: types.CallbackQuery,
    state: FSMContext
):
    language = await Users().get_user_language(jam.from_user.id)

    try:
        page = int(jam.data.split(":")[1])
        await state.update_data(page=page)
        keyboard = await get_projects_menu(page=page, language=language)
        await jam.message.edit_reply_markup(reply_markup=keyboard)

    except MessageNotModified:
        return


@dp.callback_query_handler(text="user_show_projects", state="*")
async def show_projects(jam: types.CallbackQuery, state: FSMContext):
    language = await Users().get_user_language(jam.from_user.id)
    projects_kb = await get_projects_menu(language=language)

    if projects_kb:
        message = localization.get_translation("select_project_text", language)
        await ShowProjectsStates.show_projects_for_user.set()

        start_message = (await state.get_data()).get("start_message")
        await start_message.edit_caption(
            caption=message, reply_markup=projects_kb
        )

    else:
        await jam.answer(localization.get_translation("not_active_projects_text", language), show_alert=True)


@dp.callback_query_handler(text='delete_project', state='*')
async def delete_project(jam: types.CallbackQuery, state: FSMContext):
    projects_kb = await get_projects_menu()
    if projects_kb:
        message = "💎  <b>Выберите проект для удаления:</b> "
        await jam.message.answer(message, reply_markup=projects_kb)
        await ShowProjectsStates.admin_delete_project.set()

    else:
        await jam.answer("Активных проектов не найдено 🔒", show_alert=True)


@dp.callback_query_handler(
    lambda c: c.data.startswith("project"),
    state=[
        ShowProjectsStates.show_projects_for_user,
        ShowProjectsStates.admin_delete_project,
    ],
)
async def show_selected_project(jam: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    project_id = int(jam.data.split(":")[1])
    project_data = await Projects().get_project(_id=project_id)
    language = await Users().get_user_language(jam.from_user.id)

    if current_state == ShowProjectsStates.show_projects_for_user.state:
        message = f"✨  <b>{localization.get_translation('project_name', language)}:</b> {project_data.name}\n\n"
        message += f"📚  <b>{localization.get_translation('project_description', language)}:</b>\n"
        message += f"{project_data.ru_description if language == 'ru' else project_data.en_description if language == 'en' else project_data.ua_description}\n\n"

        if project_data.link:
            message += f"🔗  <b>{localization.get_translation('project_link', language)}:</b> "
            message += f"<a href='{project_data.link}'>{localization.get_translation('go_to_project', language)}</a>\n\n"

        message += f"⏰  <b>{localization.get_translation('project_launch_date', language)}:</b> "
        message += f"{project_data.registration_date}"

        start_message = (await state.get_data()).get("start_message")
        if project_data.pictures:
            album_files = [
                types.InputMediaPhoto(await bot.download_file_by_id(file_id))
                for file_id in project_data.pictures
            ]
            album_files[0].caption = message

            album_message = await bot.send_media_group(
                chat_id=jam.from_user.id, media=album_files
            )

            cancel_message = await jam.message.answer(
                "📲", reply_markup=get_cancel_action_kb(language=language)
            )
            await start_message.delete()
            album_message.append(cancel_message)
            await state.update_data(messages_to_delete=album_message)

        else:
            info_project_message = await jam.message.answer(
                text=message, reply_markup=get_cancel_action_kb(language=language)
            )
            await start_message.delete()
            await state.update_data(messages_to_delete=[info_project_message])

        await ShowProjectsStates.show_project_details_for_user.set()

    elif current_state == ShowProjectsStates.admin_delete_project.state:
        await Projects().delete_project(_id=project_id)

        await jam.message.edit_text(
            "<b>Проект успешно удален</b> ✅", reply_markup=get_admin_projects_menu()
        )
        await MenuManagerStates.activate_projects.set()
