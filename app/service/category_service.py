from models.category import Category


class CategoryService:

    @staticmethod
    async def create_category(category_info: dict):
        await Category.create(**category_info)

    @staticmethod
    async def delete_all():
        await Category.all().delete()
