import io

from aiogram import types

from loader import dp
from database import Users
from keyboards import get_admin_users_txt_kb
from states import MenuManagerStates


@dp.callback_query_handler(text="admin_manage_users", state="*")
async def admin_manage_users(jam: types.CallbackQuery):
    users_statistic = await Users().get_users_statistics()

    text = f"""
    💎 <b>Количество зарегистрированных пользователей за:</b>
    
    - <b>сегодня:</b> <code>{users_statistic['count_users_today']}</code>
    - <b>вчера:</b> <code>{users_statistic['count_users_yesterday']}</code>
    - <b>неделю:</b> <code>{users_statistic['count_users_week']}</code>
    - <b>месяц:</b> <code>{users_statistic['count_users_month']}</code>
    - <b>все время:</b> <code>{users_statistic['summary_count_users']}</code>
    """

    await jam.message.edit_text(text, reply_markup=get_admin_users_txt_kb())
    await MenuManagerStates.activate_users.set()


@dp.callback_query_handler(
    text="get_users_in_txt", state=MenuManagerStates.activate_users
)
async def get_users_in_txt(jam: types.CallbackQuery):
    users = await Users().get_all_users()
    user_data = "\n".join(
        f"User ID: {user[0]} | Username: {user[1]} | Registered at: {user[2]}"
        for user in users
    )

    file_buffer = io.BytesIO(user_data.encode())
    file_buffer.seek(0)
    file_name = "users.txt"
    document = types.InputFile(file_buffer, filename=file_name)
    await jam.message.answer_document(document)
