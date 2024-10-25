from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.open_chat import router as open_chat_router


app = FastAPI()
app.include_router(open_chat_router)

origins = [
    "http://localhost:5173",
    "http://localhost:4173",
    "https://chat-ro.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)