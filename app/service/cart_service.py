from models.cart import Cart


class CartService:

    @staticmethod
    async def create_cart(cart_info: dict):
        await Cart.create(**cart_info)

    @staticmethod
    async def get_cart(cart_id: int):
        return await Cart.get(id=cart_id)

    @staticmethod
    async def update_cart(cart_id: int, cart_info: dict):
        await Cart.filter(id=cart_id).update(**cart_info)

    @staticmethod
    async def delete_cart(cart_id: int):
        await Cart.filter(id=cart_id).delete()

    @staticmethod
    async def get_cart_list(user_id: int):
        return await Cart.filter(user_id=user_id).all()
