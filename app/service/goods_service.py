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
