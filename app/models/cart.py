from tortoise import fields

from models import BaseModel


class Cart(BaseModel):
    """
    购物车表
    """
    user = fields.ForeignKeyField('models.User', related_name='cart_user')
    product = fields.ForeignKeyField('models.Product', related_name='cart_product')
    quantity = fields.IntField()
    selected = fields.BooleanField(default=True, description="是否选中")

    class Meta:
        table = "cart"
