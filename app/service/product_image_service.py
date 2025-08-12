from models.product_image import ProductImage


class ProductImageService:

    @staticmethod
    async def delete_all():
        await ProductImage.all().delete()

    @staticmethod
    async def create(product_image):
        await ProductImage.create(**product_image)

    @staticmethod
    async def get_by_product_id(product_id):
        return await ProductImage.filter(product_id=product_id).all()

    @staticmethod
    async def delete_by_product_id(product_id):
        await ProductImage.filter(product_id=product_id).delete()
