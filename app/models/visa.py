from tortoise import fields

from models import BaseModel


class VisaUser(BaseModel):
    """
    签证用户表
    """
    last_name = fields.CharField(max_length=100)
    first_name = fields.CharField(max_length=100)
    province = fields.CharField(max_length=50)
    id_number = fields.CharField(max_length=50)
    passport = fields.CharField(max_length=50)
    address = fields.CharField(max_length=100)
    phone = fields.CharField(max_length=20)
    email = fields.CharField(max_length=100)
    gender = fields.CharField(max_length=20)
    issue_date = fields.DateField()
    expiration_date = fields.DateField()
    birth_date = fields.DateField()

    class Meta:
        table = "visa_users"
