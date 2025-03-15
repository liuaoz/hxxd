from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from config.jwt_config import JWT_TOKEN_HEAD
from core.response import JsonRet
from service.login_service import login
from service.user_service import UserService
from util.jwt_util import verify_token

login_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class LoginRequest(BaseModel):
    code: str
    encryptedData: str
    iv: str


@login_router.post("/loginByCode")
async def login_by_code(login_info: LoginRequest):
    code = login_info.code
    encrypted_data = login_info.encryptedData
    iv = login_info.iv
    token, username = await login(code, encrypted_data, iv)

    return JsonRet(data={
        'token': token,
        'tokenHead': JWT_TOKEN_HEAD,
        'username': username,
    })


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    openid = payload.get("sub")
    if openid is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await UserService.get_user_by_openid(openid)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@login_router.get("/info")
async def get_user_info(user=Depends(get_current_user)):
    return JsonRet(code=400, data={
        'username': '测试',
    })
