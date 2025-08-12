import logging
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from core.response import JsonRet
from models.address import Address
from router.login_router import get_current_user
from service.address_service import AddressService

address_router = APIRouter()


class AddressRequest(BaseModel):
    id: Optional[int] = None
    name: str
    phone: str
    province: str
    city: str
    district: str
    detail: str
    defaultStatus: int = 0

    def to_db_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "province": self.province,
            "city": self.city,
            "district": self.district,
            "detail": self.detail,
            "default_status": self.defaultStatus
        }

    @classmethod
    def from_db(cls, address: Address):
        return cls(
            id=address.id,
            name=address.name,
            phone=address.phone,
            province=address.province,
            city=address.city,
            district=address.district,
            detail=address.detail,
            defaultStatus=address.default_status
        )


@address_router.get("/list")
async def get_address_list(user=Depends(get_current_user)):
    addresses = await AddressService.get_address_list(user.id)
    addresses = [AddressRequest.from_db(address) for address in addresses]
    return JsonRet(data=addresses)


@address_router.get("/default")
async def get_default_address(user=Depends(get_current_user)):
    address = await AddressService.get_default_address(user.id)
    return JsonRet(data=AddressRequest.from_db(address) if address else None)


@address_router.get("/{address_id}")
async def get_address(address_id: int, user=Depends(get_current_user)):
    logging.log(logging.INFO, f"Fetching address with ID: {address_id} for user: {user.id}")

    address_info = await AddressService.get_address(address_id)
    return JsonRet(data=AddressRequest.from_db(address_info) if address_info else None)


@address_router.post("")
async def create_address(address: AddressRequest, user=Depends(get_current_user)):
    address_info = address.to_db_dict()
    address_info['user_id'] = user.id
    await AddressService.create_address(address_info, user.id)
    return JsonRet(data=address_info)


@address_router.put("/{address_id}")
async def update_address(address: AddressRequest, user=Depends(get_current_user)):
    address_info = address.to_db_dict()
    await AddressService.update_address(address.id, address_info, user.id)
    return JsonRet(data=address_info)


@address_router.delete("/{address_id}")
async def delete_address(address_id: int, user=Depends(get_current_user)):
    await AddressService.delete_address(address_id, user.id)
    return JsonRet(data={"message": "Address deleted successfully"})
