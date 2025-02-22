from fastapi import APIRouter

user_router = APIRouter()


# create user
@user_router.post("/user")
async def create_user():
    return {"msg": "create user"}


# get user
@user_router.get("/user/{user_id}")
async def get_user(user_id: int):
    return {"msg": "get user", "user_id": user_id}


# update user
@user_router.put("/user")
async def update_user():
    return {"msg": "update user"}


# delete user
@user_router.delete("/user")
async def delete_user():
    return {"msg": "delete user"}
