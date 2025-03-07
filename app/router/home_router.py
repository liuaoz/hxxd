import base64

from fastapi import APIRouter

from config.base_config import SERVER_HOST
from core.response import JsonRet
from service.file_service import FileService

home_router = APIRouter()


@home_router.get("/content")
async def home():
    return JsonRet(message='Hello World', data={
        "advertiseList": [
            {
                'pic': 'http://127.0.0.1:8080/static/image/logo.png',
            },
            {
                'pic': 'http://127.0.0.1:8080/static/image/logo.png'}
        ],
        "hotProductList": [
        ]
    })


@home_router.get("/productCateList/{category_id}")
async def get_categories(category_id: int):
    icon_files = await FileService.get_goods_categories_icons()

    return JsonRet(message='get categories',
                   data=[
                       {
                           'icon_url': f'{SERVER_HOST}/file/1',
                           'icon': 'icon-beike',
                           'id': icon.id,
                           'name': '贝壳',
                       } for icon in icon_files
                   ]
                   )
