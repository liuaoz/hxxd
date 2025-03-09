from fastapi import APIRouter

from core.response import JsonRet
from service.goods_service import GoodsService

good_router = APIRouter()


@good_router.get("/list")
async def get_goods_list():
    return JsonRet(data=await GoodsService.get_goods_list())


# 根据商品类别和分页条件，获取商品列表
@good_router.get("/search")
async def get_goods_list_by_category(category_id: int, page: int = 1, size: int = 10):
    goods = await GoodsService.get_goods_list_by_category_page(category_id, page, size)
    return JsonRet(data=goods)
