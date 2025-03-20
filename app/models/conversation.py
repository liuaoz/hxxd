from tortoise import fields

from models import BaseModel


class Conversation(BaseModel):
    """
    会话表
    """
    session_id = fields.CharField(max_length=255)
    conversation_id = fields.CharField(max_length=255)
    # 消息类型: text, image, voice, video, file, event
    message_type = fields.CharField(max_length=255, default='text', description='消息类型: text, image, voice, video')
    content = fields.TextField()
    # 发送者: user, bot
    sender = fields.CharField(max_length=255, description='发送者: user, bot')
    bot_id = fields.IntField(null=True)
    user = fields.ForeignKeyField('models.User', related_name='conversation_user')

    class Meta:
        table = "conversation"
