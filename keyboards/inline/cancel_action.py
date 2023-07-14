from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import localization


def get_cancel_action_kb(language: str = 'ru'):
    cancel_action_bt = InlineKeyboardButton(text=localization.get_translation('cancel_action', language), callback_data="cancel_action")
    cancel_action_kb = InlineKeyboardMarkup().add(cancel_action_bt)
    return cancel_action_kb
