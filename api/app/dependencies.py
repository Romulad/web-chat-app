from typing_extensions import Annotated

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, Request, status, HTTPException, WebSocketException, WebSocket
from bson import ObjectId

from .utils.db import get_db_from_request
from .utils.security import validate_user_token
from .database import db_collection_names
from .schemas import UserWithId


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign-in")


async def get_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    request: Request
):
    user_id = validate_user_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    db = get_db_from_request(request)
    collection = db.get_collection(db_collection_names.users)

    if not (user_data := await collection.find_one({"_id": ObjectId(user_id)})):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User could not be found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UserWithId(**user_data)


async def get_socket_user(
    token: str, 
    request: WebSocket
) -> UserWithId:    
    exception = WebSocketException(
        code=status.WS_1008_POLICY_VIOLATION,
        reason="Could not validate credentials",
    )

    if not token:
        raise exception
    
    user_id = validate_user_token(token)
    if not user_id:
        raise exception

    db = get_db_from_request(request)
    collection = db.get_collection(db_collection_names.users)

    if not (user_data := await collection.find_one({"_id": ObjectId(user_id)})):
        raise exception

    return UserWithId(**user_data)
