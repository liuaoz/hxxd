from fastapi import APIRouter

from config.jwt_config import JWT_TOKEN_HEAD
from core.response import JsonRet
from service.login_service import login

login_router = APIRouter()


@login_router.post("/loginByCode")
async def login_by_code(login_info: dict):
    code = login_info.get("code")
    encrypted_data = login_info.get("encryptedData")
    iv = login_info.get("iv")
    token, username = await login(code, encrypted_data, iv)

    return JsonRet(data={
        'token': token,
        'tokenHead': JWT_TOKEN_HEAD,
        'username': username,
    })


@login_router.get("/info")
async def get_user_info():
    return JsonRet(code=400, data={
        'username': '测试',
    })
