from tortoise import fields

from models import BaseModel


class User(BaseModel):
    """
    用户表, 微信小程序用户
    """
    id = fields.IntField(pk=True)
    phone = fields.CharField(max_length=11)
    nick_name = fields.CharField(max_length=50)
    open_id = fields.CharField(max_length=50)
    union_id = fields.CharField(max_length=50)

    class Meta:
        table = "users"
