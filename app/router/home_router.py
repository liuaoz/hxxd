from fastapi import APIRouter

from config.base_config import SERVER_HOST, get_url
from constant.file_constant import FileUsageType
from core.response import JsonRet
from service.category_service import CategoryService
from service.file_service import FileService
from service.home_banner_service import HomeBannerService
from service.product_service import ProductService

home_router = APIRouter()


@home_router.get("/tab_bar")
async def get_tab_bar():
    data = [
        {
            "index": 0,
            "text": '首页',
            "iconPath": f'{SERVER_HOST}/file/100',
            "selectedIconPath": f'{SERVER_HOST}/file/200'
        },
        {
            "index": 1,
            "text": '客服',
            "iconPath": f'{SERVER_HOST}/file/300',
            "selectedIconPath": f'{SERVER_HOST}/file/400'
        }, {
            "index": 2,
            "text": '购物车',
            "iconPath": f'{SERVER_HOST}/file/500',
            "selectedIconPath": f'{SERVER_HOST}/file/600'
        }, {
            "index": 3,
            "text": '我',
            "iconPath": f'{SERVER_HOST}/file/700',
            "selectedIconPath": f'{SERVER_HOST}/file/800'
        },

    ]

    return JsonRet(message='get tab bar', data=data)


@home_router.get("/content")
async def home():
    products = await ProductService.get_hot_product_list()

    home_banners = await HomeBannerService.get_all()
    advertise_list = [
        {
            'pic': get_url(banner.file_id),
        } for banner in home_banners
    ]
    return JsonRet(message='Hello World', data={
        'advertiseList': advertise_list,
        'hotProductList': [{
            'id': product.id,
            'name': product.title,
            'price': product.price,
            'pic': get_url(product.main_image_file_id),
            'detail': product.detail,
        }
            for product in products
        ],
        'notice': '海鲜干货，敬请收藏'
    })


@home_router.get("/productCateList")
async def get_categories():
    categories = await CategoryService.get_all()

    data = [
        {
            'icon': get_url(category.file_id),
            'id': category.id,
            'name': category.name,
        } for category in categories
    ]

    return JsonRet(message='get categories', data=data)
