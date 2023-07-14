from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_admin_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="Проекты", callback_data="admin_projects"),
        InlineKeyboardButton(text="Пользователи", callback_data="admin_manage_users"),
    )
    keyboard.add(
        InlineKeyboardButton(text="Рассылка", callback_data="admin_broadcast"),
        InlineKeyboardButton(
            text="Юзер меню", callback_data="admin_switch_to_user_menu"
        ),
    )
    return keyboard


def get_admin_projects_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text="Добавить новый проект", callback_data="add_new_project"
        )
    )
    keyboard.add(
        InlineKeyboardButton(text="Удалить проект", callback_data="delete_project")
    )
    keyboard.add(InlineKeyboardButton(text="« Назад", callback_data="cancel_action"))
    return keyboard


def get_admin_accept_media_files_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Готово", callback_data="pictures_loaded"))
    keyboard.add(InlineKeyboardButton(text="« Назад", callback_data="cancel_action"))
    return keyboard


def get_admin_project_link_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="Пропустить", callback_data="skip_project_link")
    )
    keyboard.add(InlineKeyboardButton(text="« Назад", callback_data="cancel_action"))
    return keyboard


def get_admin_users_txt_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="📥  Скачать TXT  📥", callback_data="get_users_in_txt")
    )
    keyboard.add(InlineKeyboardButton(text="« Назад", callback_data="cancel_action"))
    return keyboard


def get_admin_broadcaster_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="Обычная рассылка", callback_data="text_broadcast")
    )
    keyboard.add(
        InlineKeyboardButton(text="Рассылка с видео", callback_data="video_broadcast")
    )
    keyboard.add(
        InlineKeyboardButton(text="Рассылка с фото", callback_data="photo_broadcast")
    )
    keyboard.add(InlineKeyboardButton(text="« Назад", callback_data="cancel_action"))
    return keyboard
