from datetime import datetime, timedelta
from tortoise import Model, fields


class Users(Model):
    user_id = fields.IntField()
    username = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    language = fields.TextField(default='ru')

    async def add_user(self, user_id: int, username: str, language: str) -> bool:
        if not await self.filter(user_id=user_id).exists():
            await self.create(user_id=user_id, username=username, language=language)
            return True

        return False

    async def get_users_statistics(self) -> dict:
        return {
            "summary_count_users": await self.all().count(),
            "count_users_today": await self.filter(
                created_at__gte=datetime.now().date()
            ).count(),
            "count_users_yesterday": await self.filter(
                created_at__gte=datetime.now().date() - timedelta(days=1)
            ).count(),
            "count_users_week": await self.filter(
                created_at__gte=datetime.now().date() - timedelta(days=7)
            ).count(),
            "count_users_month": await self.filter(
                created_at__gte=datetime.now().date() - timedelta(days=30)
            ).count(),
        }

    async def get_all_users(self) -> list:
        return await self.all().values_list("user_id", "username", "created_at")


    async def get_user_language(self, user_id: int) -> str | None:
        user = await self.filter(user_id=user_id).get()
        if user:
            return user.language
        return None
