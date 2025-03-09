from config.db_config import init_db2
from init.data import CATEGORIES
from service.category_service import CategoryService


async def init_category():
    await init_db2()
    await CategoryService.delete_all()
    for category in CATEGORIES:
        await CategoryService.create_category(category)


async def init_goods():
    pass

if __name__ == '__main__':
    import asyncio

    asyncio.run(init_category())
