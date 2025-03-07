from fastapi import APIRouter

from service.address_service import AddressService

address_router = APIRouter()


@address_router.get("/list")
async def get_address_list():

    await AddressService.get_address_list(user_id)
    return {"address": "address"}


@address_router.get("/{address_id}")
async def get_address(address_id: int):
    return {"address": "address"}


@address_router.post("/")
async def create_address():
    return {"address": "address"}


@address_router.put("/")
async def update_address(address_id: int):
    return {"address": "address"}
