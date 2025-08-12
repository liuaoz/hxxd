import json
from typing import List

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from core.response import JsonRet
from router.login_router import get_current_user
from service.cart_service import CartService

cart_router = APIRouter()


class AddRequest(BaseModel):
    productId: int
    quantity: int


class CartIdsRequest(BaseModel):
    cartIds: list[int]


@cart_router.get("/list")
async def get_cart_list(user=Depends(get_current_user)):
    items = await CartService.get_cart_list(user.id)

    return JsonRet(data=items)


@cart_router.post("")
async def add_to_cart(request: AddRequest, user=Depends(get_current_user)):
    await CartService.add_to_cart(user.id, request.productId, request.quantity)
    return JsonRet(message="添加到购物车成功")


@cart_router.put("/selected/{selected}")
async def update_cart_selected(selected: bool, body: CartIdsRequest, user=Depends(get_current_user)):
    await CartService.selected_cart(user.id, body.cartIds, selected)
    return JsonRet(message="更新购物车选中状态成功")


@cart_router.delete("/{cart_id}")
async def delete_cart(cart_id: int, user=Depends(get_current_user)):
    await CartService.delete_cart(cart_id, user.id)
    return JsonRet(message="删除购物车成功")


@cart_router.put("/{cart_id}/{quantity}")
async def update_cart_quantity(cart_id: int, quantity: int, user=Depends(get_current_user)):
    await CartService.update_cart_quantity(user.id, cart_id, quantity)
    return JsonRet(message="更新购物车数量成功")


@cart_router.get("/count")
async def get_cart_count(user=Depends(get_current_user)):
    count = await CartService.get_cart_count(user.id)
    return JsonRet(data={"count": count})
