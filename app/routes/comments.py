from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import get_comments_by_user,get_comments_for_post, create_comment, update_comment, delete_comment
from app.database import get_session
from app.schemas import CommentRead, CommentCreate
from typing import List

from app.auth.oauth2 import get_current_user
from app.models import User

router = APIRouter()

@router.post("/create_comment", response_model=CommentRead)
async def comment_create(
    comment: CommentCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    new_comment = await create_comment(comment, db, user_id=current_user.id)
    return new_comment

@router.get("/user_comments/{user_id}", response_model=List[CommentRead])
async def get_user_comments(user_id:int,db:AsyncSession = Depends(get_session)):
    return await get_comments_by_user(user_id,db)

@router.get("/post_comments/{post_id}",response_model=List[CommentRead])
async def get_post_comments(post_id:int,db:AsyncSession = Depends(get_session)):
    return await get_comments_for_post(post_id,db)


@router.put("/update_comment/{comment_id}", response_model=CommentRead)
async def update_existing_comment(comment_id:int,comment_data : CommentCreate, db:AsyncSession = Depends(get_session),current_user:User = Depends(get_current_user)):
    return await update_comment(comment_id,comment_data,db)

@router.delete("/delete_comment/{comment_id}")
async def delete_existing_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return await delete_comment(comment_id, db)