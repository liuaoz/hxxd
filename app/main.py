# fastapi
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config.db_config import init_db
from config.log_config import setup_logging
from router import user_router, home_router, login_router, file_router, address_router, cart_router

setup_logging()

app = FastAPI()

init_db(app)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router.user_router)
app.include_router(home_router.home_router, prefix="/home")
app.include_router(login_router.login_router, prefix="/sso")
app.include_router(file_router.file_router, prefix="/file")

app.include_router(address_router.address_router, prefix="/address")

app.include_router(cart_router.cart_router, prefix="/cart")

if __name__ == '__main__':
    uvicorn.run(app='app.main:app', host="localhost", port=8080, reload=False)
