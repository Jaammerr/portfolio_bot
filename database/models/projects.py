import json

from tortoise import Model, fields
from utils import translate_text


class Projects(Model):
    name = fields.CharField(max_length=255)
    ru_description = fields.TextField()
    en_description = fields.TextField()
    ua_description = fields.TextField()
    pictures = fields.JSONField(null=True)
    link = fields.TextField(null=True)
    registration_date = fields.TextField()

    async def add_project(
        self,
        name: str,
        description: str,
        pictures: list,
        link: str,
        registration_date: str,
    ):
        pictures_json = json.dumps(pictures)
        ua_desc_translation = translate_text(description, "ua")
        en_desc_translation = translate_text(description, "en")

        await self.create(
            name=name,
            ru_description=description,
            en_description=en_desc_translation,
            ua_description=ua_desc_translation,
            pictures=pictures_json,
            link=link if link else None,
            registration_date=registration_date,
        )

    async def get_project(self, _id: int):
        project = await self.get(id=_id)
        return project

    async def get_projects(self) -> list:
        projects = await self.all().values(
            "id", "name", "description", "pictures", "link", "registration_date"
        )
        return projects

    async def delete_project(self, _id: int) -> bool:
        if self.filter(id=_id).exists():
            await self.filter(id=_id).delete()
            return True

        return False
