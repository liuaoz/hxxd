from models.cart import Cart
from service.product_service import ProductService


class CartService:

    @staticmethod
    async def get_cart_count(user_id: int):
        """
        获取购物车商品总数量
        :param user_id: 用户ID
        :return: 商品总数量
        """
        return await Cart.filter(user_id=user_id).count()

    @staticmethod
    async def update_cart_quantity(user_id: int, cart_id: int, quantity: int):
        """
        更新购物车商品数量
        :param user_id: 用户ID
        :param cart_id: 购物车ID
        :param quantity: 商品数量
        """
        if quantity <= 0:
            await Cart.filter(id=cart_id, user_id=user_id).delete()
        else:
            await Cart.filter(id=cart_id, user_id=user_id).update(quantity=quantity)

    @staticmethod
    async def selected_cart(user_id: int, cart_ids: list[int], selected: bool):
        """
        更新购物车选中状态
        :param user_id: 用户ID
        :param cart_ids: 购物车ID列表
        :param selected: 是否选中
        """
        if not cart_ids:
            return
        await Cart.filter(user_id=user_id, id__in=cart_ids).update(selected=selected)

    @staticmethod
    async def add_to_cart(user_id: int, product_id: int, quantity: int):
        existing_cart = await Cart.filter(user_id=user_id, product_id=product_id).first()
        if existing_cart:
            existing_cart.quantity += quantity
            await existing_cart.save()
        else:
            await Cart.create(user_id=user_id, product_id=product_id, quantity=quantity)

    @staticmethod
    async def get_cart_list(user_id: int):
        carts = await Cart.filter(user_id=user_id).all()

        if not carts:
            return []

        product_ids = [cart.product_id for cart in carts]

        products = await ProductService.get_by_ids(product_ids)

        cart_items = []
        for cart in carts:
            product = next((p for p in products if p.id == cart.product_id), None)
            if product:
                cart_items.append({
                    "id": cart.id,
                    "product_id": product.id,
                    "product_title": product.title,
                    "product_sub_title": product.sub_title,
                    "price": product.price,
                    "quantity": cart.quantity,
                    "selected": cart.selected,
                    "total_price": product.price * cart.quantity
                })

        return cart_items

    @staticmethod
    async def get_carts(user_id: int):
        return await Cart.filter(user_id=user_id).all()

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
    async def delete_cart(cart_id: int, user_id: int):
        await Cart.filter(id=cart_id, user_id=user_id).delete()
