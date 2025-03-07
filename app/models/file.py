from tortoise import fields

from constant.file_constant import FileUsageType
from models import BaseModel


class File(BaseModel):
    """
    文件表
    """
    file_name = fields.CharField(max_length=100)
    bucket_name = fields.CharField(max_length=100)
    path = fields.CharField(max_length=100)
    usage_type = fields.CharField(max_length=50, comment=f"{','.join([item.value for item in FileUsageType])}")

    class Meta:
        table = "file"
