from typing_extensions import Annotated

from fastapi import APIRouter, Request, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas import UserWithPassword, UserWithId
from ..database import db_collection_names
from ..response_model import Token
from ..utils.security import create_user_token, verify_password
from ..utils.db import get_db_from_request
from ..dependencies import get_user

router = APIRouter(prefix="/auth")


@router.post("/sign-up", response_model=Token, status_code=status.HTTP_201_CREATED)
async def create_account(user: UserWithPassword, request: Request):
    collection = get_db_from_request(request).get_collection(
        db_collection_names.users
    )

    # check if an user with that email already exist
    if await collection.find_one({"email": user.email}):
        raise HTTPException(409, "Email already exists")

    new_user = await collection.insert_one(user.model_dump())
    access_token = create_user_token(str(new_user.inserted_id))

    return {"access_token": access_token}


@router.post("/sign-in", response_model=Token)
async def login(
    request:Request, 
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_email = form_data.username
    user_password = form_data.password

    db = get_db_from_request(request)
    user_collection = db.get_collection(db_collection_names.users)

    if not (user_data := await user_collection.find_one({"email": user_email})):
        raise exception
    
    if not verify_password(user_password, user_data.get('password', "")):
        raise exception
    
    user_id = str(user_data['_id'])
    access_token = create_user_token(user_id)

    return {"access_token": access_token}


@router.get("/me", response_model=UserWithId)
async def about_user(user: Annotated[UserWithPassword, Depends(get_user)]):
    return user