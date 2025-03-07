from constant.file_constant import FileUsageType
from models.file import File
from service.minio_service import MinioService


class FileService:

    @staticmethod
    async def get_file_content(file_id: int):
        file = await File.get(id=file_id)
        return MinioService.get_file(file.bucket_name, file.path)

    @staticmethod
    async def get_goods_categories_icons():
        return await File.filter(usage_type=FileUsageType.GOODS_CATEGORY_ICON.value).all()
