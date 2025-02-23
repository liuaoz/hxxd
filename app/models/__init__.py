from tortoise import fields, Model


class BaseModel(Model):
    id = fields.IntField(pk=True)
    create_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)
    remark = fields.TextField(null=True)

    class Meta:
        abstract = True
