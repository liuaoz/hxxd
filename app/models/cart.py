from tortoise import fields

from models import BaseModel


class Cart(BaseModel):
    """
    购物车表
    """
    user = fields.ForeignKeyField('models.User', related_name='cart_user')
    goods = fields.ForeignKeyField('models.Product', related_name='cart_product')
    quantity = fields.IntField()

    class Meta:
        table = "cart"
