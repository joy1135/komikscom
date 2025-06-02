from fastapi import FastAPI, HTTPException, Depends, APIRouter, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import label, select, desc, func, asc, nullslast, delete
from sqlalchemy.orm import selectinload, noload
from sqlalchemy.dialects.postgresql import insert as pg_insert
import models as m
from typing import List, Optional
import pyd
from sqlalchemy.sql.functions import coalesce
from auth import get_current_user

router = APIRouter(
    prefix="/comm",
    tags=["comm"],
)

@router.get("/{comic_id}/comments", response_model=List[pyd.CommentBase])
async def get_comments(comic_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(m.Comment).where(m.Comment.comicID == comic_id).options(selectinload(m.Comment.user))
    )
    comments = result.scalars().all()
    return comments

@router.post("/{comic_id}/comments", response_model=pyd.CommentBase)
async def create_comment(
    comic_id: int,
    comment_data: pyd.CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: m.User = Depends(get_current_user)
):
    comment = m.Comment(
        comicID=comic_id,
        userID=current_user.id,
        comment=comment_data.comment
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment

@router.post("/{comic_id}/rate", response_model=pyd.RatingBase)
async def rate_comic(
    comic_id: int,
    rating_data: pyd.RatingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: m.User = Depends(get_current_user)
):
    result = await db.execute(
        select(m.Rating).where(
            m.Rating.comic_id == comic_id,
            m.Rating.user_id == current_user.id
        )
    )
    rating = result.scalar_one_or_none()

    if rating:
        rating.value = rating_data.value
    else:
        rating = m.Rating(
            comic_id=comic_id,
            user_id=current_user.id,
            value=rating_data.value
        )
        db.add(rating)

    await db.commit()
    await db.refresh(rating)
    return rating
