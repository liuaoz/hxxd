import os

from minio import Minio

MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT')
MINIO_PORT = os.getenv('MINIO_PORT')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')


def get_minio_client():
    return Minio(
        f"{MINIO_ENDPOINT}:{MINIO_PORT}",
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )
