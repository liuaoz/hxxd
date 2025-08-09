import asyncio

from config.db_config import init_db2
from constant.constant import BOT_ID
from constant.conversation_message import Sender, MessageType
from models.conversation import Conversation
from util.util import generate_uuid


class ConversationService:

    @staticmethod
    async def generate_session_id():
        return generate_uuid()

    @staticmethod
    async def conversation(message, user_id, session_id=None):
        conversation_id = generate_uuid()
        session_id = session_id if session_id else await ConversationService.generate_session_id()
        await ConversationService.create_user_message(message, user_id, session_id, conversation_id)

        # 测试，随机生成回复
        await asyncio.sleep(1)
        response = '您好，我是您的购物助手，目前正在开发中，敬请期待！'

        bot_resp = await ConversationService.create_bot_message(response, user_id, session_id, conversation_id)
        return {
            'id': bot_resp.id,
            'session_id': session_id,
            'conversation_id': conversation_id,
            'sender': Sender.BOT.value,
            'content': response
        }

    @staticmethod
    async def create_bot_message(content, user_id, session_id, conversation_id):
        conversation_info = {
            'message_type': MessageType.TEXT.value,
            'sender': Sender.BOT.value,
            'bot_id': BOT_ID,
            'user_id': user_id,
            'session_id': session_id,
            'conversation_id': conversation_id,
            'content': content
        }
        return await Conversation.create(**conversation_info)

    @staticmethod
    async def create_user_message(content, user_id, session_id, conversation_id):
        conversation_info = {
            'message_type': MessageType.TEXT.value,
            'sender': Sender.USER.value,
            'user_id': user_id,
            'session_id': session_id,
            'conversation_id': conversation_id,
            'content': content
        }
        await Conversation.create(**conversation_info)

    @staticmethod
    async def get_messages_by_session_id(session_id, user_id):
        if not session_id:
            return await ConversationService.get_latest_session_messages(user_id)
        return await Conversation.filter(session_id=session_id).order_by('create_time')

    @staticmethod
    async def get_latest_session_messages(user_id):
        latest_session_message = await Conversation.filter(user_id=user_id).order_by('-create_time').first()
        if latest_session_message:
            latest_session_id = latest_session_message.session_id
            return await Conversation.filter(user_id=user_id, session_id=latest_session_id).order_by('create_time')
        return []


async def test():
    await init_db2()
    items = await ConversationService.get_latest_session_messages(1)
    print(items)


if __name__ == '__main__':
    asyncio.run(test())
