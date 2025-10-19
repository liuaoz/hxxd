from models.visa import VisaUser


class VisaUserService:

    @staticmethod
    async def add(user: dict):

        id_number = user.get('id_number')
        passport = user.get('passport')
        if await VisaUser.filter(id_number=id_number).exists() or await VisaUser.filter(passport=passport).exists():
            await VisaUser.filter(id_number=id_number).update(**user)
        else:
            await VisaUser.create(**user)

    @staticmethod
    async def list_all():
        users = await VisaUser.all().order_by("-create_time")
        return [user for user in users]
