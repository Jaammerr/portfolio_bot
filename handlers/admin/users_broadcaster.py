from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import MenuManagerStates, BroadcasterStates
from keyboards import get_admin_menu, get_cancel_action_kb
from database import Users


@dp.callback_query_handler(
    text=[
        "text_broadcast",
        "video_broadcast",
        "photo_broadcast",
    ],
    state=MenuManagerStates.activate_broadcaster,
)
async def admin_get_type_of_broadcast(jam: types.CallbackQuery, state: FSMContext):
    await state.update_data(broadcast_type=jam.data)
    if jam.data == "text_broadcast":
        message = "📝  <b>Введите текст рассылки:</b>"
        await BroadcasterStates.wait_for_broadcaster_text.set()

    elif jam.data == "photo_broadcast":
        message = "🖼  <b>Отправьте фото для рассылки:</b>"
        await BroadcasterStates.wait_for_broadcaster_photo.set()

    else:
        message = "🎥  <b>Отправьте видео для рассылки:</b>"
        await BroadcasterStates.wait_for_broadcaster_video.set()

    await jam.message.edit_text(message, reply_markup=get_cancel_action_kb())


@dp.message_handler(
    content_types="photo", state=BroadcasterStates.wait_for_broadcaster_photo
)
async def admin_get_photo_for_broadcast(jam: types.Message, state: FSMContext):
    await state.update_data(photo=jam.photo[-1].file_id)
    await jam.answer("📝  <b>Введите текст рассылки:</b>", reply_markup=get_cancel_action_kb())

    await BroadcasterStates.wait_for_broadcaster_text.set()


@dp.message_handler(
    content_types=["video", "gif", "animation"],
    state=BroadcasterStates.wait_for_broadcaster_video,
)
async def admin_get_video_for_broadcast(jam: types.Message, state: FSMContext):
    if jam.content_type == "animation":
        await state.update_data(video=jam.animation.file_id)

    else:
        await state.update_data(video=jam.video.file_id)

    await jam.answer("📝  <b>Введите текст рассылки:</b>", reply_markup=get_cancel_action_kb())
    await BroadcasterStates.wait_for_broadcaster_text.set()


@dp.message_handler(state=BroadcasterStates.wait_for_broadcaster_text)
async def admin_get_text_for_broadcast(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await start_broadcaster(message, state)


async def start_broadcaster(jam: types.Message, state: FSMContext):
    state_data = await state.get_data()
    users = await Users().get_all_users()
    text = state_data["text"]

    if state_data["broadcast_type"] == "text_broadcast":
        for user in users:
            try:
                await bot.send_message(chat_id=user[0], text=text)
            except:
                continue

    elif state_data["broadcast_type"] == "photo_broadcast":
        for user in users:
            try:
                await bot.send_photo(chat_id=user[0], photo=state_data["photo"], caption=text)
            except Exception as e:
                continue

    else:
        for user in users:
            try:
                await bot.send_video(chat_id=user[0], video=state_data["video"], caption=text)
            except:
                continue

    await jam.answer("Рассылка успешно завершена!", reply_markup=get_admin_menu())
    await state.finish()
