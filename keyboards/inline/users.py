from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import localization


def get_users_menu(language: str):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text=localization.get_translation('portfolio_bt', language), callback_data="user_show_projects")
    )
    keyboard.add(
        InlineKeyboardButton(text=localization.get_translation('about_us_bt', language), callback_data="user_show_about_us"),
        InlineKeyboardButton(text='FAQ ❓', callback_data="user_show_faq")
    )
    keyboard.add(
        InlineKeyboardButton(text=localization.get_translation('services_bt', language), callback_data="user_show_services"),
        InlineKeyboardButton(text=localization.get_translation('contact_us_bt', language), url="https://t.me/Jaammerr"),
    )
    return keyboard



def get_locales_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="UA", callback_data="set_language_ua"),
        InlineKeyboardButton(text="RU", callback_data="set_language_ru"),
        InlineKeyboardButton(text="EN", callback_data="set_language_en"),
    )
    return keyboard
