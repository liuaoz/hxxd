from models.address import Address


class AddressService:

    @staticmethod
    async def get_default_address(user_id: int):
        """
        获取用户默认地址
        :param user_id: 用户ID
        :return: 默认地址对象或None
        """
        return await Address.filter(user_id=user_id, default_status=1).first()

    @staticmethod
    async def create_address(address_info: dict, user_id: int):
        address_info.pop('id', None)

        exists_addresses = await AddressService.get_address_list(user_id)

        if address_info.get('default_status') == 1:
            for addr in exists_addresses:
                if addr.default_status == 1:
                    addr.default_status = 0
                    await addr.save()
        elif not exists_addresses:
            address_info['default_status'] = 1
        await Address.create(**address_info)

    @staticmethod
    async def get_address(address_id: int):
        return await Address.get(id=address_id)

    @staticmethod
    async def update_address(address_id: int, address_info: dict, user_id: int):
        address_info.pop('id', None)
        address_info['user_id'] = user_id

        # 设置默认地址
        if address_info.get('default_status') == 1:
            exists_addresses = await AddressService.get_address_list(user_id)
            for addr in exists_addresses:
                if addr.default_status == 1 and addr.id != address_id:
                    addr.default_status = 0
                    await addr.save()
        elif not await Address.filter(user_id=user_id, default_status=1).exists():
            address_info['default_status'] = 1

        await Address.filter(id=address_id).update(**address_info)

    @staticmethod
    async def delete_address(address_id: int, user_id: int):
        # 设置默认地址
        address = await Address.get(id=address_id)
        if address.default_status == 1:
            exists_addresses = await Address.filter(user_id=user_id).exclude(id=address_id).all()
            if exists_addresses:
                first_address = exists_addresses[0]
                first_address.default_status = 1
                await first_address.save()
        await Address.filter(id=address_id).delete()

    @staticmethod
    async def get_address_list(user_id: int):
        return await Address.filter(user_id=user_id).all()
