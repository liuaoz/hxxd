import logging

from config.minio_config import get_minio_client


class MinioService:
    @staticmethod
    def upload_file(file, bucket_name, object_name):
        """
        上传文件
        :param file: 文件对象
        :param bucket_name: 桶名称
        :param object_name: 对象名称
        :return:
        """
        client = get_minio_client()
        try:
            client.fput_object(bucket_name, object_name, file.file, file.file.filename)
            return True
        except Exception as e:
            logging.error("upload file error: %s", e)
            return False

    @staticmethod
    def get_file(bucket_name, object_name):
        """
        获取文件
        :param bucket_name: 桶名称
        :param object_name: 对象名称
        :return:
        """
        client = get_minio_client()
        try:
            return client.get_object(bucket_name, object_name)
        except Exception as e:
            logging.error("get file error: %s", e)
            return None
