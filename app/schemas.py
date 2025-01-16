from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # class Config:
    #     orm_mode = True


class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # here by this class we get the alchemy sql model and we need to convert it into the pydantic model so convert into it we will the
    # class config
    class Config:
        orm_mode = True
        
class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True  # Use orm_mode for older versions


class UserCreate(BaseModel):
    email: EmailStr
    password: str





class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
