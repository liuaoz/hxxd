from tortoise.query_utils import Q

from models.user import User


class UserService:

    @staticmethod
    async def register_user(phone, openid):
        if not await UserService.exists_user(openid, phone):
            await UserService.create_user(phone, openid)
        return await UserService.get_user_by_phone(phone)

    @staticmethod
    async def exists_user(openid, phone):
        return await User.filter(Q(phone=phone) | Q(openid=openid)).exists()

    @staticmethod
    async def create_user(phone, openid):
        user = {
            "phone": phone,
            "openid": openid,
            "nickname": phone,
        }
        await User.create(**user)

    @staticmethod
    async def get_user(user_id: int):
        return await User.get(id=user_id)

    @staticmethod
    async def update_user(user_id: int, user_info: dict):
        await User.filter(id=user_id).update(**user_info)

    @staticmethod
    async def delete_user(user_id: int):
        await User.filter(id=user_id).delete()

    @staticmethod
    async def get_user_by_phone(phone):
        return await User.get(phone=phone)

    @staticmethod
    async def get_user_by_openid(openid):
        return await User.get(openid=openid)
