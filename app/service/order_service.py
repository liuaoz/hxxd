import time

from tortoise.transactions import atomic

from constant.order_enum import OrderPayType, OrderStatus
from models.order import Order
from models.order_item import OrderItem
from service.order_item_service import OrderItemService
from service.pay_service import WxPayService
from service.address_service import AddressService
from service.cart_service import CartService
from service.product_service import ProductService
from service.user_service import UserService
from util.order_util import generate_out_trade_no
from util.util import generate_order_no


class OrderService:

    @staticmethod
    @atomic()
    async def cancel_order(user_id: int, order_id: int):
        order = await Order.get(id=order_id, user_id=user_id)
        if not order:
            raise ValueError("订单不存在或不属于当前用户")

        if order.status != OrderStatus.PENDING_PAYMENT.value:
            raise ValueError("订单状态不允许取消")

        order.status = OrderStatus.CANCELED.value
        await order.save()

        # 这里可以添加库存回退逻辑
        order_items = await OrderItemService.get_by_order_id(order_id)
        for item in order_items:
            product = await ProductService.get(item.product_id)
            if product:
                product.stock += item.quantity
                await product.save()

    @staticmethod
    async def get_orders(user_id: int, status: int = 0, page: int = 1, page_size: int = 10):

        if status == -1:
            orders = await Order.filter(user_id=user_id).offset((page - 1) * page_size).limit(page_size).order_by(
                '-create_time').all()
        else:
            orders = await Order.filter(user_id=user_id, status=status).offset((page - 1) * page_size).limit(
                page_size).order_by('-create_time').all()

        order_ids = [order.id for order in orders]
        orders_items = await OrderItemService.get_by_order_ids(order_ids)
        order_list = []
        for order in orders:
            order_items = [item for item in orders_items if item.order_id == order.id]
            order_data = {
                "id": order.id,
                "order_no": order.order_no,
                "status": order.status,
                "payment_type": order.payment_type,
                "recipient_name": order.recipient_name,
                "recipient_phone": order.recipient_phone,
                "recipient_address": order.recipient_address,
                "total_amount": order.total_amount,
                "create_time": int(time.mktime(order.create_time.timetuple())),
                "items": [
                    {
                        "product_id": item.product_id,
                        "product_title": item.product_title,
                        "product_main_file_id": item.product_main_file_id,
                        "quantity": item.quantity,
                        "price": item.price
                    } for item in order_items
                ]
            }
            order_list.append(order_data)
        return order_list

    @staticmethod
    async def generate_confirm_order(user_id: int):
        # 这里实现生成确认订单的逻辑
        pass

    @staticmethod
    async def prepay(user_id: int, order_id: int):
        order = await Order.get(id=order_id, user_id=user_id)
        if not order:
            raise ValueError("订单不存在或不属于当前用户")

        user = await UserService.get_user(user_id)

        if order.status != OrderStatus.PENDING_PAYMENT.value:
            raise ValueError("订单状态不允许预支付")

        out_trade_no = generate_out_trade_no(order.order_no, order.out_trade_no)

        order.out_trade_no = out_trade_no

        await Order.save(order)

        return await WxPayService.prepay(out_trade_no, order.total_amount, user.openid, 'test_description')

    @staticmethod
    @atomic()
    async def create_order(user_id: int, address_id: int):
        address = await AddressService.get_address(address_id)
        selected_carts = await CartService.get_selected_carts(user_id)

        if not selected_carts:
            raise ValueError("没有选中的购物车商品")

        if not address:
            raise ValueError("地址不存在")

        product_ids = [cart.product_id for cart in selected_carts]
        products = await ProductService.get_by_ids(product_ids)

        total_amount = 0
        for cart in selected_carts:

            product = next((p for p in products if p.id == cart.product_id), None)
            if not product:
                raise ValueError(f"商品ID {cart.product_id} 不存在")
            if product.stock < cart.quantity:
                raise ValueError(f"商品 {product.title} 库存不足")
            total_amount += product.price * cart.quantity

        order_param = {
            "user_id": user_id,
            "order_no": generate_order_no(),
            "address_id": address_id,

            "status": OrderStatus.PENDING_PAYMENT.value,
            "payment_type": OrderPayType.WECHAT.value,

            "recipient_name": address.name,
            "recipient_phone": address.phone,
            "recipient_address": f"{address.province} {address.city} {address.district} {address.detail}",
            "total_amount": total_amount
        }

        order = await Order.create(**order_param)

        order_item = [
            {
                "order_id": order.id,
                "product_id": cart.product_id,
                "product_title": next((p.title for p in products if p.id == cart.product_id), ""),
                "product_main_file_id": next((p.main_image_file_id for p in products if p.id == cart.product_id), 0),
                "quantity": cart.quantity,
                "price": next((p.price for p in products if p.id == cart.product_id), 10000),
            }
            for cart in selected_carts
        ]

        await OrderItem.bulk_create([OrderItem(**item) for item in order_item])

        # await CartService.clear_selected_carts(user_id)

        return order.id
