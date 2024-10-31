from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.open_chat import router as open_chat_router
from .settings import IN_PRODUCTION


app = FastAPI(
    description="""Backend for a chat application that let `people chat in a open way`.\n
    1- Create a chat
    2- Share link to invite people to join
    3- Confirm join requests
    4- Chat
    5- Once done click delete, to delete everything""", 
    title="Open chat",
    summary="Server for a chat application" 
)
app.include_router(open_chat_router)


if IN_PRODUCTION:
    origins = [
        "https://chat-ro.onrender.com",
    ]
else:
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