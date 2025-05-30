from datetime import date
from typing import List
from pydantic import BaseModel, Field, EmailStr, field_validator
from pyd import *
import re

class GenreCreate(GenreBase):
    pass

class RoleCreate(RoleBase):
    pass

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nick: str

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Пароль должен быть больше 8 символов")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r"[a-z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву")
        if not re.search(r"\d", v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        return v

class ComicCreate(ComicBase):
    userID: int = Field(..., example=1)
    genre_ids: List[int] = Field(default=[], example=[1, 2])
    
    volume_ids: List[int] = Field(default=[], example=[1, 2])
    chapter_ids: List[int] = Field(default=[], example=[1, 2])

class CommentCreate(CommentBase):
    userID: int = Field(..., example=1)
    comicID: int = Field(..., example=1)

class RatingCreate(RatingBase):
    user_id: int = Field(..., example=1)
    comic_id: int = Field(..., example=1)

class PageCreate(BaseModel):
    volume_id: int = Field(..., example=1)  
    chapter_id: int = Field(..., example=1) 
    number: int = Field(..., example=1)  
    image_url: str = Field(..., example="comics/Комикс 1/comic/vl1/ch1/1.jpg")

class ChapterCreate(BaseModel):
    volume_id: int = Field(..., example=1)  
    number: int = Field(..., example=1)  
    title: str = Field(..., example="Глава 1") 

    pages: List[PageCreate] = []

class VolumeCreate(BaseModel):
    number: int = Field(..., example=1)
    chapters: List[ChapterCreate] = []

