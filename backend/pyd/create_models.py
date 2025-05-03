from datetime import date
from typing import List
from pydantic import Field
from pyd import *

class GenreCreate(GenreBase):
    pass

class RoleCreate(RoleBase):
    pass

class UserCreate(UserBase):
    password: str = Field(..., example="securepassword123", max_length=255)
    roleId: int = Field(..., example=1)

class ComicCreate(ComicBase):
    userID: int = Field(..., example=1)
    genre_ids: List[int] = Field(default=[], example=[1, 2])

class CommentCreate(CommentBase):
    userID: int = Field(..., example=1)
    comicID: int = Field(..., example=1)

class RatingCreate(RatingBase):
    user_id: int = Field(..., example=1)
    comic_id: int = Field(..., example=1)