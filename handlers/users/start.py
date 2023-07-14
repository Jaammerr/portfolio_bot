from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from loader import dp, bot, localization
from keyboards import get_users_menu, get_admin_menu, get_locales_menu
from data import admins
from database import Users


@dp.message_handler(CommandStart(), state="*")
async def bot_start(jam: types.Message, state: FSMContext):
    await state.finish()

    if jam.from_user.id not in admins:
        if not await Users().filter(user_id=jam.from_user.id).exists():
            await jam.answer(
                '📲  <b>Оберіть мову / Выберите язык / Choose language:</b> ',
                reply_markup=get_locales_menu()
            )
            await jam.delete()

        else:
            await send_start_message(user_id=jam.from_user.id, state=state)


    else:
        await Users().add_user(
            user_id=jam.from_user.id,
            username=jam.from_user.username,
            language='ru'
        )
        await jam.answer("💎  <b>Админ-панель:</b>", reply_markup=get_admin_menu())


@dp.callback_query_handler(
    lambda call: call.data.startswith("set_language")
)
async def set_language(jam: types.CallbackQuery, state: FSMContext):
    language = jam.data.split("_")[2]

    if not await Users().filter(user_id=jam.from_user.id).exists():
        await Users().add_user(
            user_id=jam.from_user.id,
            username=jam.from_user.username,
            language=language
        )
    else:
        await Users().filter(user_id=jam.from_user.id).update(language=language)

    await send_start_message(user_id=jam.from_user.id, state=state)
    await jam.message.delete()


async def send_start_message(user_id: int, state: FSMContext):
    state_data = await state.get_data()
    language = await Users().get_user_language(user_id=user_id)

    if 'start_message' not in state_data:
        with open("./image1.jpg", "rb") as photo:
            message = await bot.send_photo(
                chat_id=user_id, photo=photo, reply_markup=get_users_menu(language)
            )
            await state.update_data(start_message=message)

    else:
        start_message = state_data["start_message"]

        await start_message.edit_caption(
            caption='',
            reply_markup=get_users_menu(language)
        )



@dp.message_handler(
    commands="change_language",
    state='*'
)
async def change_language(jam: types.Message, state: FSMContext):
    await state.finish()

    await jam.answer(
        '📲  <b>Оберіть мову / Выберите язык / Choose language:</b> ',
        reply_markup=get_locales_menu()
    )
    await jam.delete()
