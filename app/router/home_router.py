from fastapi import APIRouter

from config.base_config import SERVER_HOST
from constant.file_constant import FileUsageType
from core.response import JsonRet
from service.file_service import FileService
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
    files = await FileService.get_file_by_usage_type(FileUsageType.HOME_LUN_BO)
    goods = await ProductService.get_hot_product_list()
    advertise_list = [
        {
            'pic': f'{SERVER_HOST}/file/{file.id}',
        } for file in files
    ]
    return JsonRet(message='Hello World', data={
        'advertiseList': advertise_list,
        'hotProductList': [{
            'id': good.id,
            'name': good.title,
            'price': good.price,
            'pic': f'{SERVER_HOST}/file/{good.main_image}',
            'detail': good.detail,
        }
            for good in goods
        ],
        'notice': '海鲜干货，敬请收藏'
    })


@home_router.get("/productCateList/{category_id}")
async def get_categories(category_id: int):
    files = await FileService.get_product_categories_icons()

    data = [
        {
            'icon': f'{SERVER_HOST}/file/{file.id}',
            'id': file.id,
            'name': file.remark,
        } for file in files
    ]

    return JsonRet(message='get categories', data=data)
