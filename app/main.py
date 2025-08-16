# fastapi
import traceback

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from config.db_config import init_db
from config.log_config import setup_logging
from core.response import JsonRet
from router import user_router, home_router, login_router, file_router, address_router, cart_router, chat_router, \
    product_router, order_router

setup_logging()

app = FastAPI()

init_db(app)


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        # 记录完整的错误堆栈
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content=JsonRet(code=500, message="服务器内部错误").to_dict()
        )


# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router.user_router)
app.include_router(home_router.home_router, prefix="/home")
app.include_router(login_router.login_router, prefix="/sso")
app.include_router(file_router.file_router, prefix="/file")

app.include_router(address_router.address_router, prefix="/address")

app.include_router(cart_router.cart_router, prefix="/cart")

app.include_router(chat_router.chat_router, prefix="/chat")

app.include_router(product_router.product_router, prefix="/product")

app.include_router(order_router.order_router, prefix="/order")

if __name__ == '__main__':
    uvicorn.run(app='app.main:app', host="0.0.0.0", port=8080, reload=False)
