from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.open_chat import router as open_chat_router
from .settings import OROGINS


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
app.add_middleware(
    CORSMiddleware,
    allow_origins=OROGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)