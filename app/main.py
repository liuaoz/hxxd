# fastapi
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config.db_config import init_db
from config.log_config import setup_logging
from router import user_router, home_router

setup_logging()

app = FastAPI()

init_db(app)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router.user_router)
app.include_router(home_router.home_router, prefix="/home")

if __name__ == '__main__':
    uvicorn.run(app='app.main:app', host="localhost", port=8080, reload=False)
