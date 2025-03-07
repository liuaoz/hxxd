from fastapi import APIRouter, Depends

from core.response import JsonRet
from router.login_router import get_current_user
from service.cart_service import CartService

cart_router = APIRouter()


@cart_router.get("/list")
async def get_cart_list(user=Depends(get_current_user)):

    items = await CartService.get_cart_list(user.id)

    return JsonRet(data=items)
