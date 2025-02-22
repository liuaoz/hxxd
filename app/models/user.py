from tortoise import Model, fields


class User(Model):
    id = fields.IntField(pk=True)
    phone = fields.CharField(max_length=11)
    nick_name = fields.CharField(max_length=50)

    class Meta:
        table = "users"
