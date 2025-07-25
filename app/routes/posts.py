from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import create_post, get_post_by_id,get_all_posts, update_post, delete_post
from app.database import get_session
from app.schemas import PostCreate, PostRead, PostUpdate
from typing import List

from app.auth.oauth2 import get_current_user
from app.models import User

router = APIRouter()


@router.get("/test")
def test_route():
    return {"message": "Post router working"}


# @router.post("/create_post", response_model = PostRead)
# async def create_post(post: PostCreate,db : AsyncSession = Depends(get_session)):
#     return await create_post(post,db)

# only logged-in users with a valid token can create posts
@router.post("/create_post",response_model = PostRead)
async def create_post_handler(
    post:PostCreate,
    db : AsyncSession = Depends(get_session),
    current_user : User = Depends(get_current_user)
):
    return await create_post(post,db,current_user)

@router.get("/{id}",response_model = PostRead)
async def get_post(id:int, db: AsyncSession=Depends(get_session)):
    return await get_post_by_id(id,db)

# @router.get("/search_post")

@router.get("/",response_model=List[PostRead])
async def all_posts(db : AsyncSession = Depends(get_session),current_user : User = Depends(get_current_user)):
    return await get_all_posts(db)


@router.patch("/update_post/{id}")
async def post_update(
    id : int,
    post:PostUpdate,
    db : AsyncSession = Depends(get_session),
    current_user : User = Depends(get_current_user)
):
    return await update_post(id,post,db)

@router.delete("/delete_post/{id}")
async def post_delete(
    id : int,
    db : AsyncSession = Depends(get_session),
    current_user : User = Depends(get_current_user)
):
    return await delete_post(id, db)