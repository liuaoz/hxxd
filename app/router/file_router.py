from fastapi import APIRouter

from core.response import JsonRet
from service.file_service import FileService
from fastapi.responses import StreamingResponse

file_router = APIRouter()


@file_router.get("/{file_id}")
async def get_file(file_id: int):
    image_data = await FileService.get_file_content(file_id)
    return StreamingResponse(image_data, media_type="image/jpeg")
