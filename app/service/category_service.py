from models.category import Category


class CategoryService:

    @staticmethod
    async def create(category_info: dict):
        await Category.create(**category_info)

    @staticmethod
    async def delete_all():
        await Category.all().delete()

    @staticmethod
    async def get_all():
        return await Category.all()
