from fastapi import APIRouter

from core.response import JsonRet

home_router = APIRouter()


@home_router.get("/content")
async def home():
    return JsonRet(message='Hello World', data={
        "advertiseList":
            [
                {
                    'pic': 'http://127.0.0.1:8080/static/image/logo.png',
                },
                {
                    'pic': 'http://127.0.0.1:8080/static/image/logo.png'}
            ]})


@home_router.get("/productCateList/{id}")
async def get_categories(id: int):
    return JsonRet(message='get categories',
                   data={
                       "id": id,
                       "icon": "xia",
                       "name": "虾",
                   })
