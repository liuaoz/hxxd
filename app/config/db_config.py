import importlib
import os
import pkgutil

from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

HOST = os.getenv("DB_HOST", "localhost")
USER_NAME = os.getenv("DB_USER", "postgres")
PASSWORD = os.getenv("DB_PASSWORD", "111111")
DB_NAME = os.getenv("DB_NAME", "postgres")
PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"postgres://{USER_NAME}:{PASSWORD}@{HOST}/{DB_NAME}"


def discover_models(package):
    models = []
    package_dir = os.path.dirname(importlib.import_module(package).__file__)
    for _, module_name, _ in pkgutil.iter_modules([package_dir]):
        models.append(f"{package}.{module_name}")
    return models


model_modules = discover_models("models")

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": model_modules,  # 指定模型文件路径
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



async def init_db2():
    """
    for test
    """
    await Tortoise.init(
        db_url=DATABASE_URL,  # 使用 SQLite 作为示例
        modules={'models': model_modules}  # 如果是当前文件，使用 '__main__'
    )
    await Tortoise.generate_schemas()  # 生成数据库表
