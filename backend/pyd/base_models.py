from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class GenreBase(BaseModel):
    name: str = Field(..., example="Fantasy", max_length=255)

class RoleBase(BaseModel):
    name: str = Field(..., example="Admin", max_length=255)

class UserBase(BaseModel):
    email: str = Field(..., example="user@example.com", max_length=255)
    nick: str = Field(..., example="cool_user", max_length=255)

class ComicBase(BaseModel):
    id: int
    title: str = Field(..., example="Shrek", max_length=255)
    desc: Optional[str] = Field(None, example="Awesome Comic", max_length=255)
    date_of_out: date = Field(..., example="2023-01-15")
    website_recommendation: bool = Field(..., example=True)
    img: str =Field(...)
    average_rating: Optional[float] = None

    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    comment: str = Field(..., example="Great comic!", max_length=255)

class RatingBase(BaseModel):
    value: int = Field(..., ge=0, le=10, example=8)

class PageResponse(BaseModel):
    id: int
    number: int = Field(..., example=1)
    image_url: str = Field(..., example="comics/Комикс 1/comic/vl1/ch1/1.jpg")

    class Config:
        from_attributes = True

class ChapterResponse(BaseModel):
    id: int
    number: int = Field(..., example=1)
    title: Optional[str] = Field(None, example="Начало")
    pages: List[PageResponse] = []

    class Config:
        from_attributes = True

class VolumeResponse(BaseModel):
    id: int
    number: int = Field(..., example=1)
    chapters: List[ChapterResponse] = []

    class Config:
        from_attributes = True

class GenreResponse(GenreBase):
    id: int = Field(..., example=1)
    class Config:
        from_attributes = True

class RoleResponse(RoleBase):
    id: int = Field(..., example=1)
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    email: str
    nick: str

    class Config:
        from_attributes = True

class ComicResponse(ComicBase):
    id: int = Field(..., example=1)
    userID: int = Field(..., example=1)
    average_rating: Optional[float] = Field(None, example=4.5)
    user: UserResponse
    genres: List[GenreResponse] = []
    volumes: List[VolumeResponse] = []

    class Config:
        from_attributes = True

class CommentResponse(CommentBase):
    id: int = Field(..., example=1)
    created_at: datetime = Field(..., example="2023-01-15T12:00:00")
    user: UserResponse
    comic: ComicBase
    class Config:
        from_attributes = True

class RatingResponse(RatingBase):
    id: int = Field(..., example=1)
    rated_at: datetime = Field(..., example="2023-01-15T12:00:00")
    user: UserBase
    comic: ComicBase
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class UserLogin(BaseModel):
    email: str
    password: str

UserResponse.model_rebuild()
ComicResponse.model_rebuild()
