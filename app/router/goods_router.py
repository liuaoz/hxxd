from fastapi import APIRouter, Path

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


@good_router.get("/{goods_id}")
async def get_goods_detail(goods_id: int):
    goods = await GoodsService.get_goods(goods_id)
    return JsonRet(data=goods)


@good_router.get("/image/list/{goods_id}")
async def get_goods_images(goods_id: int):
    goods = await GoodsService.get_goods(goods_id)
    if not goods:
        return JsonRet(code=404, message="商品不存在")
    return JsonRet(data=goods.images)
