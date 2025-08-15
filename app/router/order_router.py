from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from constant.url_constant import ORDER_PAY_SUCCESS_NOTIFY
from core.response import JsonRet
from service.order_service import OrderService
from router.login_router import get_current_user

order_router = APIRouter()


class OrderCreateRequest(BaseModel):
    addressId: int


@order_router.get("/list")
async def list_orders(request: Request, user=Depends(get_current_user)):
    params = request.query_params
    page = int(params.get("pageNum", 1))
    page_size = int(params.get("pageSize", 10))
    status = int(params.get("status", 0))  # 默认状态为0，表示所有状态

    orders = await OrderService.get_orders(user.id, status=status, page=page, page_size=page_size)
    return JsonRet(data=orders, message="订单列表获取成功")


# 支付成功通知
@order_router.post(ORDER_PAY_SUCCESS_NOTIFY)
async def pay_success_notify(request: Request):
    """
    支付成功通知
    :param request: 请求体
    :return: JsonRet
    """
    body = await request.body()
    # 这里应该调用订单服务的支付成功通知方法
    # 例如：await OrderService.pay_success_notify(body)
    return JsonRet(message="支付成功通知处理成功")


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


@order_router.post("/prepay/{order_id}")
async def prepay(order_id: int, user=Depends(get_current_user)):
    """
    预支付
    :param user: 当前用户
    :return: JsonRet
    """
    # 这里应该调用订单服务的预支付方法
    await OrderService.prepay(user.id, order_id)
    return JsonRet(message="预支付成功")


@order_router.post("/generateOrder")
async def generate_order(body: OrderCreateRequest, user=Depends(get_current_user)):
    print(body.addressId)
    order_id = await OrderService.create_order(user.id, body.addressId)
    return JsonRet(data={"id": order_id}, message="订单生成成功")
