from fastapi import APIRouter, Depends
from pydantic import BaseModel

from core.response import JsonRet
from models.order_service import OrderService
from router.login_router import get_current_user

order_router = APIRouter()


class OrderCreateRequest(BaseModel):
    addressId: int


@order_router.post("/generateConfirmOrder")
async def generate_confirm_order(user=Depends(get_current_user)):
    """
    生成确认订单
    :param user: 当前用户
    :return: JsonRet
    """
    # 这里应该调用订单服务的生成确认订单方法
    # 例如：await OrderService.generate_confirm_order(user.id)
    return JsonRet(message="确认订单生成成功")


@order_router.post("/prepay")
async def prepay(user=Depends(get_current_user)):
    """
    预支付
    :param user: 当前用户
    :return: JsonRet
    """
    # 这里应该调用订单服务的预支付方法
    # 例如：await OrderService.prepay(user.id)
    return JsonRet(message="预支付成功")


@order_router.post("/generateOrder")
async def generate_order(body: OrderCreateRequest, user=Depends(get_current_user)):
    address_id = body.addressId
    await OrderService.create_order(user.id, address_id)
    return JsonRet(message="订单创建成功")
