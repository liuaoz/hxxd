from models.order_item import OrderItem


class OrderItemService:

    @staticmethod
    async def get_by_order_id(order_id: int):
        return await OrderItem.filter(order_id=order_id).all()

    @staticmethod
    async def get_by_order_ids(order_ids: list[int]):
        return await OrderItem.filter(order_id__in=order_ids).all()
