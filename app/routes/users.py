from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import create_user, get_user_by_email, get_user_by_id, login_user, delete_user, update_user
from app.database import get_session
from app.schemas import UserCreate, UserLogin, UserRead, UserUpdate
from app.models import User
from app.auth.oauth2 import get_current_user

router = APIRouter()

@router.get("/hello")
async def say_hello():
    return {"message": "Hello from user router"}

@router.post("/register", response_model=UserRead)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    return await create_user(user,db)


@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_session)):
    return await login_user(user,db)

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/{id}",response_model = UserRead)
async def get_user(id:int, db:AsyncSession = Depends(get_session)):
    return await get_user_by_id(id,db)

@router.patch("/{id}")
async def user_updation(id : int, user_update: UserUpdate,db:AsyncSession = Depends(get_session)):
    return await update_user(id,user_update,db)

@router.delete("/{id}")
async def user_delete(id : int, db : AsyncSession = Depends(get_session)):
    return await delete_user(id,db)