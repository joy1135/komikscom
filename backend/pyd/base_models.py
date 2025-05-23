from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, conint

class GenreBase(BaseModel):
    name: str = Field(..., example="Fantasy", max_length=255)

class RoleBase(BaseModel):
    name: str = Field(..., example="Admin", max_length=255)

class UserBase(BaseModel):
    email: str = Field(..., example="user@example.com", max_length=255)
    nick: str = Field(..., example="cool_user", max_length=255)

class ComicBase(BaseModel):
    title: str = Field(..., example="Awesome Comic", max_length=255)
    image: str = Field(..., example="comic1.jpg", max_length=255)
    date_of_out: date = Field(..., example="2023-01-15")
    website_recommendation: bool = Field(..., example="True")

class CommentBase(BaseModel):
    comment: str = Field(..., example="Great comic!", max_length=255)

class RatingBase(BaseModel):
    value: int = Field(..., ge=0, le=10, example=8)

class GenreResponse(GenreBase):
    id: int = Field(..., example=1)
    
    class Config:
        from_attributes = True

class RoleResponse(RoleBase):
    id: int = Field(..., example=1)
    
    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int = Field(..., example=1)
    role: 'RoleResponse'
    
    class Config:
        from_attributes = True

class ComicResponse(ComicBase):
    id: int = Field(..., example=1)
    userID: int = Field(..., example=1)
    average_rating: Optional[float] = Field(None, example=4.5, ge=0, le=10)
    user: UserResponse
    genres: List[GenreResponse] = Field(default=[])
    
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

UserResponse.model_rebuild()
ComicResponse.model_rebuild()