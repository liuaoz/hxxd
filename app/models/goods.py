from tortoise import fields

from models import BaseModel


class Goods(BaseModel):
    """
    商品表
    """
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=50)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    stock = fields.IntField()
    status = fields.BooleanField(default=True, description="商品状态, True: 上架, False: 下架")
    image = fields.TextField()
    detail = fields.TextField()

    class Meta:
        table = "goods"
