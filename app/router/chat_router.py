from fastapi import APIRouter, Depends

from core.response import JsonRet
from router.login_router import get_current_user
from service.conversation_service import ConversationService

chat_router = APIRouter()


@chat_router.get("/session_id")
async def get_session_id():
    return JsonRet(data=await ConversationService.generate_session_id())


@chat_router.get("/message/list")
async def get_messages(session_id: str, user=Depends(get_current_user)):
    messages = await ConversationService.get_messages_by_session_id(session_id, user.id)
    return JsonRet(data=[
        {
            'id': message.id,
            'content': message.content,
            'sender': message.sender
        }
        for message in messages]
    )


@chat_router.post("/message")
async def chat(body: dict, user=Depends(get_current_user)):
    message = body.get('message')
    session_id = body.get('session_id')
    return JsonRet(data=await ConversationService.conversation(message, user.id, session_id))
