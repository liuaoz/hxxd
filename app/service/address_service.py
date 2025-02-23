from models.address import Address


class AddressService:

    @staticmethod
    async def create_address(address_info: dict):
        await Address.create(**address_info)

    @staticmethod
    async def get_address(address_id: int):
        return await Address.get(id=address_id)

    @staticmethod
    async def update_address(address_id: int, address_info: dict):
        await Address.filter(id=address_id).update(**address_info)

    @staticmethod
    async def delete_address(address_id: int):
        await Address.filter(id=address_id).delete()

    @staticmethod
    async def get_address_list(user_id: int):
        return await Address.filter(user_id=user_id).all()
