from tortoise import fields

from models import BaseModel


class Category(BaseModel):
    """
    分类表
    """
    file_id = fields.IntField()
    code = fields.CharField(max_length=50)
    name = fields.CharField(max_length=50)
    active = fields.BooleanField(default=True, description="分类状态, True: 启用, False: 禁用")
    sort_order = fields.IntField(default=0, description="分类排序")
    parent_id = fields.IntField(description="父级分类ID")

    class Meta:
        table = "category"
