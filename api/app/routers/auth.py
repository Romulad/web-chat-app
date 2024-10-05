from fastapi import APIRouter

from ..schemas import UserWithPassword, User

router = APIRouter(prefix="/auth")

@router.post("/sign-up", response_model=User)
async def create_account(user: UserWithPassword):
    pass

