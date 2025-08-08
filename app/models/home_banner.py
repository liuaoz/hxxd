from tortoise import fields

from models import BaseModel


class HomeBanner(BaseModel):
    """
    首页轮播图表
    """
    file_id = fields.IntField(description="轮播图file_id")
    name = fields.CharField(max_length=50, description="轮播图名称")
    description = fields.CharField(max_length=200, null=True, description="轮播图描述")

    class Meta:
        table = "home_banner"
