import math

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import localization
from database import Projects


async def get_projects_menu(
    page: int = 1, page_size: int = 10, language: str = "ru"
) -> bool | InlineKeyboardMarkup:
    projects_data = await Projects().all().values("id", "name")

    if projects_data:
        markup = InlineKeyboardMarkup(row_width=1)

        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        projects_data_page = projects_data[start_index:end_index]

        for project in projects_data_page:
            markup.insert(
                InlineKeyboardButton(
                    project["name"],
                    callback_data=f'project:{project["id"]}',
                )
            )

        num_pages = math.ceil(len(projects_data) / page_size)
        if num_pages > 1:
            prev_page = page - 1 if page > 1 else 1
            next_page = page + 1 if page < num_pages else num_pages

            markup.row(
                InlineKeyboardButton(
                    "⬅️", callback_data=f"page_projects_prev:{prev_page}"
                ),
                InlineKeyboardButton(
                    f"{page}/{num_pages}", callback_data="count_pages_in_items"
                ),
                InlineKeyboardButton(
                    "➡️", callback_data=f"page_projects_next:{next_page}"
                ),
            )



        markup.add(InlineKeyboardButton(localization.get_translation('cancel_action', language), callback_data="cancel_action"))
        return markup

    else:
        return False
