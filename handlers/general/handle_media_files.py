from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states import AddNewProjectStates


@dp.message_handler(
    content_types="photo", state=[AddNewProjectStates.wait_for_media_files]
)
async def handle_photos(jam: types.Message, state: FSMContext):
    state_data = await state.get_data()

    if jam.content_type == "photo":
        file_id = jam.photo[-1].file_id

        if "media_files" in state_data:
            photo_files = state_data["media_files"]
        else:
            photo_files = []

        photo_files.append(file_id)
        await state.update_data(media_files=photo_files)
