from fastapi import FastAPI

from .database import get_db_lifespan
from .routers.auth import router as auth_router
from .routers.chat import router as chat_router
from .routers.open_chat import router as open_chat_router


app = FastAPI(lifespan=get_db_lifespan())
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(open_chat_router)