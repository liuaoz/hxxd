import asyncio

from fastapi import APIRouter

from core.response import JsonRet

user_router = APIRouter()


# create user
@user_router.post("/user")
async def create_user():
    return JsonRet(message="create user", data={"user_id": 1})


# get user
@user_router.get("/user/{user_id}")
async def get_user(user_id: int):
    return JsonRet(message="get user", data={"user_id": user_id})


# update user
@user_router.put("/user")
async def update_user():
    return JsonRet(message="update user", data={"user_id": 1})


# delete user
@user_router.delete("/user")
async def delete_user():
    return JsonRet(message="delete user", data={"user_id": 1})
