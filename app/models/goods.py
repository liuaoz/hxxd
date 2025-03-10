from tortoise import fields

from models import BaseModel


class Goods(BaseModel):
    """
    商品表
    """
    title = fields.CharField(max_length=50)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    stock = fields.IntField()
    status = fields.BooleanField(default=True, description="商品状态, True: 上架, False: 下架")
    detail = fields.TextField()
    is_hot = fields.BooleanField(default=False, description="是否是热门商品")
    category = fields.ForeignKeyField('models.Category', related_name='good_category')
    main_image = fields.IntField(description="商品主图", null=True)
    thumbnail_images = fields.JSONField(description="商品缩略图")
    detail_images = fields.JSONField(description="商品详情图")

    class Meta:
        table = "goods"
