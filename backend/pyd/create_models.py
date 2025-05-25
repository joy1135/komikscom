from datetime import date
from typing import List
from pydantic import BaseModel, Field, EmailStr, field_validator
from pyd import *
import re


# === Обновление моделей для создания ===

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

# === Модели для создания томов, глав и страниц ===

class PageCreate(BaseModel):
    volume_id: int = Field(..., example=1)  # Идентификатор тома
    chapter_id: int = Field(..., example=1)  # Идентификатор главы
    number: int = Field(..., example=1)  # Номер страницы
    image_url: str = Field(..., example="comics/Комикс 1/comic/vl1/ch1/1.jpg")  # Путь к изображению страницы

class ChapterCreate(BaseModel):
    volume_id: int = Field(..., example=1)  # Идентификатор тома
    number: int = Field(..., example=1)  # Номер главы
    title: str = Field(..., example="Глава 1")  # Название главы

    # Новое поле для страниц
    pages: List[PageCreate] = []  # Список страниц в главе

class VolumeCreate(BaseModel):
    number: int = Field(..., example=1)  # Номер тома
    chapters: List[ChapterCreate] = []  # Список глав в томе

