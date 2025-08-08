from models.product import Product


class ProductService:

    @staticmethod
    async def create_product(product_info: dict):
        await Product.create(**product_info)

    @staticmethod
    async def get_product(product_id: int):
        return await Product.get(id=product_id)

    @staticmethod
    async def get_product_list():
        return await Product.all()

    @staticmethod
    async def get_product_list_by_category_page(category_id: int, page: int = 1, size: int = 10):
        return await Product.filter(category_id=category_id).offset((page - 1) * size).limit(size).all()

    @staticmethod
    async def get_hot_product_list():
        return await Product.filter(is_hot=True).all()