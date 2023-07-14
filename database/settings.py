from tortoise import Tortoise


async def initialize_database():
    await Tortoise.init(
        db_url="sqlite://database/db.sqlite3",
        modules={"models": ["database.models.projects", "database.models.users"]},
        timezone="Europe/Moscow",
    )

    await Tortoise.generate_schemas()
