from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from database import get_db
import models as m
import pyd
from typing import List

router = APIRouter(
    prefix="/aftor",
    tags=["aftor"],
)

@router.get("/new_authors", response_model=List[pyd.UserBase])
async def get_new_authors(db: AsyncSession = Depends(get_db)):
    subquery = (
        select(
            m.Comic.userID,
            func.count(m.Comic.id).label("comics_count")
        )
        .group_by(m.Comic.userID)
        .subquery())
    last_comic_date = (
        select(
            m.Comic.userID,
            func.max(m.Comic.date_of_out).label("last_date")
        )
        .group_by(m.Comic.userID)
        .subquery())
    result = await db.execute(
        select(m.User)
        .join(
            subquery,
            m.User.id == subquery.c.userID
        )
        .join(
            last_comic_date,
            m.User.id == last_comic_date.c.userID
        )
        .where(
            and_(
                m.User.roleId.in_([1, 3]),
                subquery.c.comics_count == 1
            )
        )
        .order_by(
            last_comic_date.c.last_date.desc()
        )
    )
    
    authors = result.scalars().all()
    return authors