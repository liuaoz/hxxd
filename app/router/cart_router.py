from fastapi import APIRouter, Depends

from router.login_router import get_current_user

cart_router = APIRouter()


@cart_router.get("/list")
async def get_cart_list(user=Depends(get_current_user)):
    print(user)
    pass
