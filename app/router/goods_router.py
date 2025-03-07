from fastapi import APIRouter

from core.response import JsonRet
from service.goods_service import GoodsService

good_router = APIRouter()


@good_router.get("/list")
async def get_goods_list():
    return JsonRet(data=await GoodsService.get_goods_list())
