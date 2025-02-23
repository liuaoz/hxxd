from models.user import User


class UserService:

    @staticmethod
    async def create_user(user_info: dict):
        await User.create(**user_info)

    @staticmethod
    async def get_user(user_id: int):
        return await User.get(id=user_id)

    @staticmethod
    async def update_user(user_id: int, user_info: dict):
        await User.filter(id=user_id).update(**user_info)

    @staticmethod
    async def delete_user(user_id: int):
        await User.filter(id=user_id).delete()
