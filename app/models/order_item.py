from tortoise import fields

from models import BaseModel


class OrderItem(BaseModel):
    """
    订单详情表
    """
    order = fields.ForeignKeyField('models.Order', related_name='order_item_order')
    product = fields.ForeignKeyField('models.Product', related_name='order_item_product')

    product_title = fields.CharField(max_length=50)
    product_main_file_id = fields.IntField()
    quantity = fields.IntField()
    price = fields.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        table = "order_detail"
