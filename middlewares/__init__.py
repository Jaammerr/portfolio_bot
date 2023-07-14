from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .language_middlaware import LanguageMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
