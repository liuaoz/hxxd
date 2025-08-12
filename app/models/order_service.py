from constant.order_enum import OrderPayType, OrderStatus
from models.order import Order
from models.order_item import OrderItem
from service.address_service import AddressService
from service.cart_service import CartService
from service.product_service import ProductService


class OrderService:

    @staticmethod
    async def generate_confirm_order(user_id: int):
        # 这里实现生成确认订单的逻辑
        pass

    @staticmethod
    async def prepay(user_id: int):
        # 这里实现预支付的逻辑
        pass

    @staticmethod
    async def create_order(user_id: int, address_id: int):
        address = await AddressService.get_address(address_id)
        selected_carts = await CartService.get_selected_carts(user_id)

        if not selected_carts:
            raise ValueError("没有选中的购物车商品")

        product_ids = [cart['product_id'] for cart in selected_carts]
        products = await ProductService.get_by_ids(product_ids)

        if not address:
            raise ValueError("地址不存在")

        # 检查各个商品库存是否足够
        for cart in selected_carts:
            product = next((p for p in products if p.id == cart['product_id']), None)
            if not product:
                raise ValueError(f"商品ID {cart['product_id']} 不存在")
            if product.stock < cart['quantity']:
                raise ValueError(f"商品 {product.title} 库存不足")

        # 假设订单创建成功
        param = {
            "user_id": user_id,
            "order_no": "ORD123456789",  # 生成订单号的逻辑可以更复杂
            "address_id": address_id,

            "status": OrderStatus.PENDING_PAYMENT.value,

            "recipient_name": address.name,
            "recipient_phone": address.phone,
            "recipient_address": f"{address.province} {address.city} {address.district} {address.detail}",
            "total_amount": sum(cart['price'] * cart['quantity'] for cart in selected_carts),
        }

        # 这里可以将订单保存到数据库
        order = await Order.create(**param)

        order_item = [
            {
                "order_id": order.id,
                "product_id": cart['product_id'],
                "product_title": next((p.title for p in products if p.id == cart['product_id']), ""),
                "product_main_file_id": next((p.main_image_file_id for p in products if p.id == cart['product_id']), 0),
                "quantity": cart['quantity'],
                "price": cart['price'],
            }
            for cart in selected_carts
        ]

        # 这里可以将订单详情保存到数据库
        await OrderItem.bulk_create([OrderItem(**item) for item in order_item])

        # 清空购物车中选中商品
        await CartService.clear_selected_carts(user_id)
