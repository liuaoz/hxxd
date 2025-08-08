from config.db_config import init_db2
from init.data import CATEGORIES, FILES, PRODUCTS, HOME_BANNERS
from service.category_service import CategoryService
from service.home_banner_service import HomeBannerService
from service.product_service import ProductService


async def init_file():
    await init_db2()
    from service.file_service import FileService
    await FileService.delete_all()
    for file_info in FILES:
        await FileService.create(file_info)


async def init_category():
    await init_db2()
    await CategoryService.delete_all()
    for category in CATEGORIES:
        await CategoryService.create(category)


async def init_product():
    await init_db2()
    await ProductService.delete_all()
    for category in PRODUCTS:
        await ProductService.create(category)


async def init_home_banner():
    await init_db2()
    await HomeBannerService.delete_all()
    for banner in HOME_BANNERS:
        await HomeBannerService.create(banner)


if __name__ == '__main__':
    import asyncio

    asyncio.run(init_file())
    asyncio.run(init_category())
    asyncio.run(init_product())
    asyncio.run(init_home_banner())
