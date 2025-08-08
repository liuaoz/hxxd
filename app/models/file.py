from tortoise import fields

from models import BaseModel


class File(BaseModel):
    """
    文件表
    """
    file_name = fields.CharField(max_length=100)
    bucket_name = fields.CharField(max_length=100)
    path = fields.CharField(max_length=100)

    class Meta:
        table = "file"
