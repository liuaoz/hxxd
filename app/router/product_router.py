from fastapi import APIRouter, Request

from core.response import JsonRet
from service.product_service import ProductService

product_router = APIRouter()


@product_router.get("/list")
async def get_product_list():
    return JsonRet(data=await ProductService.get_all())


# 根据商品类别和分页条件，获取商品列表
@product_router.get("/search")
async def get_product_list_by_category(request: Request):
    params = request.query_params
    page = int(params.get("pageNum", 1))
    page_size = int(params.get("pageSize", 10))
    category_id = int(params.get("productCategoryId")) if params.get("productCategoryId") else None
    products = await ProductService.get_product_list_by_category_page(category_id, page, page_size)
    return JsonRet(data=products)


@product_router.get("/{product_id}")
async def get_product_detail(product_id: int):
    products = await ProductService.get(product_id)
    return JsonRet(data=products)


@product_router.get("/image/list/{product_id}")
async def get_product_images(product_id: int):
    products = await ProductService.get(product_id)
    if not products:
        return JsonRet(code=404, message="商品不存在")
    return JsonRet(data=products.images)
