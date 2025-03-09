from models.goods import Goods


class GoodsService:

    @staticmethod
    async def create_goods(goods_info: dict):
        await Goods.create(**goods_info)

    @staticmethod
    async def get_goods(goods_id: int):
        return await Goods.get(id=goods_id)

    @staticmethod
    async def get_goods_list():
        return await Goods.all()

    @staticmethod
    async def get_goods_list_by_category_page(category_id: int, page: int = 1, size: int = 10):
        return await Goods.filter(category_id=category_id).offset((page - 1) * size).limit(size).all()
