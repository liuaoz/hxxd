from constant.product_image import ProductImageType
from models.product import Product
from models.product_image import ProductImage


class ProductService:

    @staticmethod
    async def get_product_detail(product_id):
        """
        获取商品详情
        :param product_id: 商品ID
        :return: 商品详情
        """
        product_data = await Product.get(id=product_id).values()
        if not product_data:
            return None

        product_images = await ProductImage.filter(product_id=product_id).all()
        product_data["thumbnail_images"] = [
            img.file_id for img in product_images if img.type == ProductImageType.THUMBNAIL.value
        ]
        product_data["detail_images"] = [
            img.file_id for img in product_images if img.type == ProductImageType.DETAIL.value
        ]

        return product_data

    @staticmethod
    async def get_by_ids(product_ids: list[int]):
        return await Product.filter(id__in=product_ids).all()

    @staticmethod
    async def create(product_info: dict):
        await Product.create(**product_info)

    @staticmethod
    async def get(product_id: int):
        return await Product.get(id=product_id)

    @staticmethod
    async def get_all():
        return await Product.all()

    @staticmethod
    async def get_product_list_by_category_page(category_id: int, page: int = 1, size: int = 10):
        if category_id is None:
            return await Product.all().offset((page - 1) * size).limit(size).all()
        return await Product.filter(category_id=category_id).offset((page - 1) * size).limit(size).all()

    @staticmethod
    async def get_hot_product_list():
        return await Product.filter(is_hot=True).all()

    @staticmethod
    async def delete_all():
        await Product.all().delete()
