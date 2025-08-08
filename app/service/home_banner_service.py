from models.home_banner import HomeBanner


class HomeBannerService:

    @staticmethod
    async def create(home_banner: dict):
        await HomeBanner.create(**home_banner)

    @staticmethod
    async def delete_all():
        await HomeBanner.all().delete()

    @staticmethod
    async def get_all():
        return await HomeBanner.all()
