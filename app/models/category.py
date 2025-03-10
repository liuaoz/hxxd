from tortoise import fields

from models import BaseModel


class Category(BaseModel):
    """
    分类表
    """
    icon = fields.CharField(max_length=200)
    code = fields.CharField(max_length=50)
    name = fields.CharField(max_length=50)
    parent_id = fields.IntField()

    class Meta:
        table = "category"
