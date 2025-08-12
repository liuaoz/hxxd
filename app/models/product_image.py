from tortoise import fields

from models import BaseModel


class ProductImage(BaseModel):
    """
    商品图片表
    """
    product = fields.ForeignKeyField('models.Product', related_name='product_image_product')
    file_id = fields.IntField()
    type = fields.IntField(description="图片类型, 0: 主图, 1: 缩略图, 2: 详情图")
    sort_order = fields.IntField(default=0, description="图片排序")

    class Meta:
        table = "product_image"
