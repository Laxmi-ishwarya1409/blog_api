from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from datetime import datetime
from typing import List

class User(SQLModel,table=True):
    id : int = Field(primary_key=True)
    name : str
    email : EmailStr
    password: str = Field(nullable=False)

    posts : List["Post"] = Relationship(back_populates="user")
    comments : List["Comment"] = Relationship(back_populates = "user")


class Post(SQLModel,table=True):
    id : int = Field(primary_key=True)
    title : str
    content : str
    created_at : datetime = Field(default_factory=datetime.now)
    user_id : int = Field(foreign_key="user.id")

    user : "User" = Relationship(back_populates="posts")
    comments : List["Comment"] = Relationship(back_populates="post")


class Comment(SQLModel,table=True):
    id : int = Field(primary_key=True)
    content : str
    created_at : datetime = Field(default_factory=datetime.now)
    post_id : int = Field(foreign_key="post.id")
    user_id : int = Field(foreign_key="user.id")

    user : "User" = Relationship(back_populates="comments")
    post : "Post" = Relationship(back_populates="comments")