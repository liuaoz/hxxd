from tortoise import fields

from models import BaseModel


class Cart(BaseModel):
    """
    购物车表
    """
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='cart_user')
    goods = fields.ForeignKeyField('models.Goods', related_name='cart_goods')
    quantity = fields.IntField()
    create_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "cart"
