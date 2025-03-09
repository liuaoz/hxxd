from models.category import GoodsCategory


class CategoryService:

    @staticmethod
    async def create_category(category_info: dict):
        await GoodsCategory.create(**category_info)

    @staticmethod
    async def delete_all():
        await GoodsCategory.all().delete()
