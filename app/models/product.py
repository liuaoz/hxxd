from typing import Optional

from tortoise import fields

from models import BaseModel


class Product(BaseModel):
    """
    商品表
    """
    title = fields.CharField(max_length=50)
    sub_title = fields.TextField()
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    stock = fields.IntField()
    status = fields.IntField(description="商品状态, 0: 下架, 1: 上架")
    detail_html = fields.TextField(description="商品详情HTML")
    is_hot = fields.BooleanField(default=False, description="是否是热门商品")
    category = fields.ForeignKeyField('models.Category', related_name='product_category')
    category_id: Optional[int]
    main_image_file_id = fields.IntField(description="商品主图file_id")
    thumbnail_image_file_id = fields.IntField(description="商品缩略图file_id")

    class Meta:
        table = "product"
