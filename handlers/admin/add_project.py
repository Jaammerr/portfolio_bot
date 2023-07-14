from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards import *
from loader import dp
from states import AddNewProjectStates, MenuManagerStates
from database import Projects


@dp.callback_query_handler(
    text="add_new_project", state=MenuManagerStates.activate_projects
)
async def add_new_project(jam: types.CallbackQuery):
    await jam.message.edit_text(
        "📝  <b>Введите название проекта:</b> ", reply_markup=get_cancel_action_kb()
    )
    await AddNewProjectStates.wait_for_name.set()


@dp.message_handler(state=AddNewProjectStates.wait_for_name)
async def get_project_name(jam: types.Message, state: FSMContext):
    if await Projects().filter(name=jam.text).exists():
        await jam.answer(
            "🚫  <b>Проект с таким названием уже существует. Введите другое название:</b> ",
            reply_markup=get_cancel_action_kb(),
        )
        return

    await state.update_data(project_name=jam.text)
    await jam.answer("📝  <b>Введите описание проекта:</b> ", reply_markup=get_cancel_action_kb())
    await AddNewProjectStates.wait_for_description.set()


@dp.message_handler(state=AddNewProjectStates.wait_for_description)
async def get_project_description(jam: types.Message, state: FSMContext):
    await state.update_data(project_description=jam.text)
    await jam.answer(
        "🌅  <b>Отправьте фотографии проекта:</b> ", reply_markup=get_admin_accept_media_files_kb()
    )
    await AddNewProjectStates.wait_for_media_files.set()


@dp.callback_query_handler(
    text=["pictures_loaded", "skip_pictures_loading"],
    state=AddNewProjectStates.wait_for_media_files,
)
async def get_project_media_files(jam: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    if "media_files" not in state_data:
        await state.update_data(media_files=False)
        await jam.message.answer(
            "📝  <b>Отправьте ссылку на проект:</b> ", reply_markup=get_admin_project_link_kb()
        )
    else:
        len_loaded_media_files = len(state_data["media_files"])
        await jam.message.answer(
            f"Загружено {len_loaded_media_files} фотографии. "
            "📝  <b>Отправьте ссылку на проект:</b> ",
            reply_markup=get_admin_project_link_kb(),
        )

    await AddNewProjectStates.wait_for_link.set()


@dp.callback_query_handler(
    text="skip_project_link", state=AddNewProjectStates.wait_for_link
)
async def skip_project_link(jam: types.CallbackQuery, state: FSMContext):
    await state.update_data(project_link=False)
    await jam.message.edit_text(
        "📝  <b>Введите дату созданию проекта:</b> \n\n<code>Пример: 10:09:1974</code>",
        reply_markup=get_cancel_action_kb(),
    )
    await AddNewProjectStates.wait_for_registration_date.set()


@dp.message_handler(state=AddNewProjectStates.wait_for_link)
async def get_project_link(jam: types.Message, state: FSMContext):
    if not jam.text.startswith(("http://", "https://")):
        await jam.answer(
            "🚫  <b>Неверный формат ссылки. Попробуйте ещё раз:</b> ",
            reply_markup=get_admin_project_link_kb(),
        )
        return

    await state.update_data(project_link=jam.text)
    await jam.answer(
        "📝  <b>Введите дату создания проекта:</b> \n\n<code>Пример: 10:09:1974</code>",
        reply_markup=get_cancel_action_kb(),
    )
    await AddNewProjectStates.wait_for_registration_date.set()


@dp.message_handler(state=AddNewProjectStates.wait_for_registration_date)
async def get_project_registration_date(jam: types.Message, state: FSMContext):
    try:
        day, month, year = jam.text.split(":")
        await state.update_data(project_registration_date=jam.text)
    except ValueError:
        await jam.answer(
            "🚫  <b>Неверный формат даты. Попробуйте ещё раз:</b> \n\n<code>Пример: 10:09:1974</code>",
            reply_markup=get_cancel_action_kb(),
        )
        return

    await add_project_to_db(state)
    await jam.answer("✅  <b>Проект успешно добавлен</b>", reply_markup=get_admin_menu())
    await state.finish()


async def add_project_to_db(state_data: FSMContext):
    state_data = await state_data.get_data()

    project_name = state_data["project_name"]
    project_description = state_data["project_description"]
    project_link = state_data["project_link"]
    project_registration_date = state_data["project_registration_date"]
    media_files = state_data["media_files"]

    await Projects().add_project(
        name=project_name,
        description=project_description,
        link=project_link,
        registration_date=project_registration_date,
        pictures=media_files,
    )
