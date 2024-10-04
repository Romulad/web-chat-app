from fastapi import APIRouter

router = APIRouter(prefix="/auth")

@router.post("/sign-up")
async def create_account():
    pass

