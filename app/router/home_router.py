import base64

from fastapi import APIRouter

from config.base_config import SERVER_HOST
from constant.file_constant import FileUsageType
from core.response import JsonRet
from service.file_service import FileService

home_router = APIRouter()


@home_router.get("/content")
async def home():
    files = await FileService.get_file_by_usage_type(FileUsageType.HOME_LUN_BO)
    advertise_list = [
        {
            'pic': f'{SERVER_HOST}/file/{file.id}',
        } for file in files
    ]
    return JsonRet(message='Hello World', data={
        "advertiseList": advertise_list,
        "hotProductList": [
        ]
    })


@home_router.get("/productCateList/{category_id}")
async def get_categories(category_id: int):
    files = await FileService.get_goods_categories_icons()

    data = [
        {
            'icon': f'{SERVER_HOST}/file/{file.id}',
            'id': file.id,
            'name': file.remark,
        } for file in files
    ]

    return JsonRet(message='get categories', data=data)
