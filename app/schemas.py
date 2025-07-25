from pydantic import BaseModel
from datetime import datetime
from pydantic import EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email : EmailStr
    password : str

class UserRead(BaseModel):
    id : int
    name: str
    email : EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name : Optional[str] = None
    email : Optional[EmailStr] = None
    password : Optional[str] = None

class PostCreate(BaseModel):
    title : str
    content : str

class PostRead(BaseModel):
    id : int 
    title : str
    content : str
    created_at : datetime 
    user_id : int 

class PostUpdate(BaseModel):
    title : Optional[str] = None
    content : Optional[str] = None
    
class CommentCreate(BaseModel):
    content : str
    post_id : int

class CommentRead(BaseModel):
    id : int 
    content : str
    created_at : datetime 
    post_id : int
    user_id : int 