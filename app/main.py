# fastapi
import uvicorn
from fastapi import FastAPI

from app.config.db_config import init_db
from config.log_config import setup_logging
from router import user_router

setup_logging()

app = FastAPI()

init_db(app)

app.include_router(user_router.user_router)

if __name__ == '__main__':
    uvicorn.run(app='app.main:app', host="localhost", port=8080, reload=True)
