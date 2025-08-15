from constant.file_enum import FileUsageType
from models.file import File
from service.minio_service import MinioService


class FileService:

    @staticmethod
    async def create(file_info: dict):
        await File.create(**file_info)

    @staticmethod
    async def get_file_content(file_id: int):
        file = await File.get(id=file_id)
        return MinioService.get_file(file.bucket_name, file.path)

    @staticmethod
    async def get_product_categories_icons():
        return await File.filter(usage_type=FileUsageType.GOODS_CATEGORY_ICON.value).all()

    @staticmethod
    async def get_tab_bar_icons():
        return await File.filter(usage_type=FileUsageType.TAB_BAR_ICON.value).all()

    @staticmethod
    async def get_file_by_usage_type(usage_type: FileUsageType):
        return await File.filter(usage_type=usage_type.value).all()

    @staticmethod
    async def delete_all():
        await File.all().delete()
