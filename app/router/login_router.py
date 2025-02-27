from fastapi import APIRouter

from core.response import JsonRet
from service.login_service import login

login_router = APIRouter()


@login_router.post("/loginByCode")
async def login_by_code(login_info: dict):
    # login
    code = login_info.get("code")
    encrypted_data = login_info.get("encryptedData")
    iv = login_info.get("iv")
    r = await login(code, encrypted_data, iv)
    print(r)

    return JsonRet(data={
        'token': '',
        'tokenHead': '',
        'username': '',
    })


@login_router.get("/info")
async def get_user_info():
    return JsonRet(code=400, data={
        'username': '测试',
    })
