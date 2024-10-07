from fastapi import FastAPI

from .database import get_db_lifespan
from .routers.auth import router as auth_router

app = FastAPI(lifespan=get_db_lifespan())
app.include_router(auth_router)