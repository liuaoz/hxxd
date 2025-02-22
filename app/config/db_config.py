import os

from tortoise.contrib.fastapi import register_tortoise

HOST = os.getenv("DB_HOST", "localhost")
USER_NAME = os.getenv("DB_USER", "postgres")
PASSWORD = os.getenv("DB_PASSWORD", "111111")
DB_NAME = os.getenv("DB_NAME", "postgres")
PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"postgres://{USER_NAME}:{PASSWORD}@{HOST}/{DB_NAME}"

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["models.user"],  # 指定模型文件路径
            "default_connection": "default",
        },
    },

}


def init_db(app):
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,  # 添加异常处理器
    )
