from typing_extensions import Annotated

from fastapi import APIRouter, Request, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from ..schemas import UserWithPassword
from ..database import db_collection_names
from .response_model import Token
from ..utils.security import create_user_token, verify_password


router = APIRouter(prefix="/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign-in")


@router.post("/sign-up", response_model=Token, status_code=status.HTTP_201_CREATED)
async def create_account(user: UserWithPassword, request: Request):
    collection : AsyncIOMotorCollection = request.app.state.db.get_collection(
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

    db : AsyncIOMotorDatabase = request.app.state.db
    user_collection = db.get_collection(db_collection_names.users)

    if not (user_data := await user_collection.find_one({"email": user_email})):
        raise exception
    
    if not verify_password(user_password, user_data.get('password', "")):
        raise exception
    
    user_id = str(user_data['_id'])
    access_token = create_user_token(user_id)

    return {"access_token": access_token}