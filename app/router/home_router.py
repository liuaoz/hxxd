from fastapi import APIRouter

from core.response import JsonRet
from service.category_service import CategoryService
from service.home_banner_service import HomeBannerService
from service.product_service import ProductService

home_router = APIRouter()


@home_router.get("/tab_bar")
async def get_tab_bar():
    data = [
        {
            "index": 0,
            "text": '首页',
            "iconPath": 300,
            "selectedIconPath": 400
        },
        {
            "index": 1,
            "text": 'AI助手',
            "iconPath": 900,
            "selectedIconPath": 1000
        }, {
            "index": 2,
            "text": '购物车',
            "iconPath": 500,
            "selectedIconPath": 600
        }, {
            "index": 3,
            "text": '我',
            "iconPath": 700,
            "selectedIconPath": 800
        },

    ]

    return JsonRet(message='get tab bar', data=data)


@home_router.get("/content")
async def home():
    products = await ProductService.get_hot_product_list()

    home_banners = await HomeBannerService.get_all()
    advertise_list = [
        {
            'pic': banner.file_id,
        } for banner in home_banners
    ]
    return JsonRet(message='Hello World', data={
        'advertiseList': advertise_list,
        'hotProductList': [{
            'id': product.id,
            'title': product.title,
            'price': product.price,
            'pic': product.main_image_file_id,
            'subTitle': product.sub_title,
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
            'icon': category.file_id,
            'id': category.id,
            'name': category.name,
        } for category in categories
    ]

    return JsonRet(message='get categories', data=data)
