from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from app.auth.token import create_access_token
from app.auth.hashing import verify_password, hash_password
from app.models import User,Post,Comment
from app.schemas import UserCreate, UserLogin, UserRead, PostCreate, PostRead, CommentCreate, CommentRead, UserUpdate, PostUpdate
from app.auth.hashing import hash_password

async def login_user(user_data:UserLogin, db:AsyncSession):
    query  = select(User).where(User.email == user_data.email)
    result = await db.execute(query)
    user= result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User not found")

    if not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Incorrect Password")

    token_data = {"sub" : user.email}
    token = create_access_token(token_data)

    return {
        "access_token" : token,
        "token_type" : "bearer"
        }


async def create_user(user_data:UserCreate,db:AsyncSession,):
    query = select(User).where(User.email == user_data.email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User with this email already exists")
    
    hashed_password = hash_password(user_data.password)
    
    new_user = User(
        name = user_data.name,
        email= user_data.email,
        password=hashed_password
    )

    db.add(new_user)
    await db.commit()
    return new_user

async def get_user_by_email(email:str,db:AsyncSession):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User with this email not found")

    return user

async def get_user_by_id(user_id:int, db:AsyncSession):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User with this email not found")

    return user.model_dump()

async def update_user(user_id: int,user_update : UserUpdate, db : AsyncSession):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User not found")


    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    if update_data : 
        await db.execute(
            update(User).where(User.id == user_id).values(**update_data)
        )
        await db.commit()
        return {"message": f"User with ID {user_id} updated"}
    
    return {"message": "No changes provided"}


async def delete_user(user_id:int, db:AsyncSession):
    query = select(User). where(User.id==user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    await db.execute(delete(Comment).where(Comment.user_id == user_id))
    await db.execute(delete(Post).where(Post.user_id == user_id))
    await db.execute(delete(User).where(User.id == user_id))
    
    await db.commit()

    return {"message": f"User with ID {user_id} deleted"}

async def create_post(post_data: PostCreate, db: AsyncSession,current_user: User):
    new_post = Post(
        title=post_data.title,
        content=post_data.content,
        user_id=current_user.id
    )
    db.add(new_post)
    await db.commit()
    return new_post
    

async def get_post_by_id(post_id: int, db: AsyncSession):
    query = select(Post).where(Post.id == post_id)
    result = await db.execute(query)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post {post_id} is not found")
    
    return post

async def get_all_posts(db:AsyncSession):
    query = select(Post)
    result = await db.execute(query)
    return result.scalars().all()

# async def search_post_by_keyword(keyword : str,db:AsyncSession):

#     # query = select(Post).where(Post.content == keyword)
#     # result = await db.execute(query)
#     # return result.all()

#     # query = select(Post)
#     # if keyword not in query:
#     #     return {"message": "Not found"}
#     # result = await db.execute(query)
#     # return result.all()

async def update_post(post_id:int, post_data:PostUpdate, db:AsyncSession):
    query = select(Post).where(Post.id == post_id)
    result = await db.execute(query)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post_data.title is not None:
        post.title = post_data.title
    if post_data.content is not None:
        post.content = post_data.content
    await db.commit()
    return post

async def delete_post(post_id, db:AsyncSession):
    query = select(Post).where(Post.id == post_id)
    result = await db.execute(query)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    await db.delete(post)
    await db.commit()
    return {"message": f"Post {post_id} deleted successfully"}

async def create_comment(comment_data:CommentCreate, db: AsyncSession, user_id: int):
    new_comment = Comment(
        content=comment_data.content,
        post_id=comment_data.post_id,
        user_id=user_id
    )
    db.add(new_comment)
    await db.commit()
    return new_comment

async def get_comments_for_post(post_id:int, db: AsyncSession):
    query = select(Comment).where(Comment.post_id == post_id)
    result = await db.execute(query)
    comments = result.scalars().all()

    if not comments:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Comment not found")
    
    return comments


async def get_comments_by_user(user_id:int, db: AsyncSession):
    query = select(Comment).where(Comment.user_id == user_id)
    result = await db.execute(query)
    comments = result.scalars().all()

    if not comments:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Comment not found")
    
    return comments


async def update_comment(comment_id: int, comment_data: CommentCreate, db: AsyncSession):
    query = select(Comment).where(Comment.id == comment_id)
    result = await db.execute(query)
    comment = result.scalars().first()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    comment.content = comment_data.content
    await db.commit()
    return comment

async def delete_comment(comment_id: int, db: AsyncSession):
    query = select(Comment).where(Comment.id == comment_id)
    result = await db.execute(query)
    comment = result.scalars().first()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    await db.delete(comment)
    await db.commit()
    return {"message": "Comment deleted successfully"}