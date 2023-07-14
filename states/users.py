from aiogram.dispatcher.filters.state import StatesGroup, State


class ShowProjectsStates(StatesGroup):
    show_projects_for_user = State()
    show_project_details_for_user = State()
    admin_delete_project = State()
    active_menu = State()
