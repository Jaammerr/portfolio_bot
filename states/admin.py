from aiogram.dispatcher.filters.state import StatesGroup, State


class AddNewProjectStates(StatesGroup):
    activate = State()
    wait_for_name = State()
    wait_for_description = State()
    wait_for_media_files = State()
    wait_for_link = State()
    wait_for_registration_date = State()


class MenuManagerStates(StatesGroup):
    activate_projects = State()
    activate_users = State()
    activate_broadcaster = State()
    activate_manage_users = State()


class BroadcasterStates(StatesGroup):
    wait_for_broadcaster_text = State()
    wait_for_broadcaster_photo = State()
    wait_for_broadcaster_video = State()
