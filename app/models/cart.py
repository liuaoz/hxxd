from tortoise import fields

from models import BaseModel


class Cart(BaseModel):
    """
    购物车表
    """
    user = fields.ForeignKeyField('models.User', related_name='cart_user')
    goods = fields.ForeignKeyField('models.Goods', related_name='cart_goods')
    quantity = fields.IntField()

    class Meta:
        table = "cart"
