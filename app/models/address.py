from tortoise import fields

from models import BaseModel


class Address(BaseModel):
    """
    用户收获地址表
    """
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='address_user')
    name = fields.CharField(max_length=50)
    phone = fields.CharField(max_length=11)
    province = fields.CharField(max_length=50)
    city = fields.CharField(max_length=50)
    district = fields.CharField(max_length=50)
    detail = fields.CharField(max_length=100)
    is_default = fields.BooleanField(default=False)
    create_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "address"
