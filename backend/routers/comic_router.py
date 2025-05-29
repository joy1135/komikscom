from fastapi import FastAPI, HTTPException, Depends, APIRouter, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import label, select, desc, func, asc
from sqlalchemy.orm import selectinload, joinedload
import models as m
from typing import List, Optional
import pyd
from sqlalchemy.sql.functions import coalesce

router = APIRouter(
    prefix="/comic",
    tags=["comic"],
)

@router.get("/", response_model=List[pyd.ComicBase])
async def get_all_comics(db: AsyncSession = Depends(get_db)):
    comics = await db.execute(select(m.Comic)) 
    comics_list = comics.scalars().all()
    return comics_list

@router.get("/popular", response_model=List[pyd.ComicBase])
async def get_all_comics_popular(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(m.Comic)
        .outerjoin(m.Rating)  
        .group_by(m.Comic.id)
        .order_by(desc(func.count(m.Rating.id)))
    )
    comics = result.unique().scalars().all()
    return comics

@router.get("/comics", response_model=List[pyd.ComicBase])
async def get_comics(
    genres: List[int] = Query(default=[]),
    min_rating: Optional[float] = Query(default=None, ge=0.0, le=10.0),
    sort: Optional[str] = Query(default="avg_rating", enum=["asc", "avg_rating", "popular"]),
    db: AsyncSession = Depends(get_db)
):
    avg_rating = func.avg(m.Rating.value).label("avg_rating")
    rating_count = func.count(m.Rating.id).label("rating_count")

    stmt = select(m.Comic, avg_rating, rating_count).outerjoin(m.Rating)

    if genres:
        stmt = stmt.join(m.Comic.genres).where(m.Genre.id.in_(genres))

    stmt = stmt.group_by(m.Comic.id)

    if min_rating is not None:
        stmt = stmt.having(avg_rating >= min_rating)

    if sort == "asc":
        stmt = stmt.order_by(asc(m.Comic.title))
    elif sort == "popular":
        stmt = stmt.order_by(desc(rating_count))
    else:
        stmt = stmt.order_by(desc(avg_rating))

    stmt = stmt.options(selectinload(m.Comic.genres))

    result = await db.execute(stmt)
    rows = result.all()

    return [
        {
            **pyd.ComicBase.from_orm(row[0]).dict(),
            "average_rating": round(row[1], 2) if row[1] is not None else None,
            "rating_count": row[2]
        }
        for row in rows
    ]


@router.get("/recomm", response_model=List[pyd.ComicBase])
async def get_all_comics_reccom(db: AsyncSession = Depends(get_db)):
    comics = await db.execute(select(m.Comic).where(m.Comic.website_recommendation == True))
    comics_list = comics.scalars().all()
    return comics_list

@router.get("/new_5", response_model=List[pyd.ComicBase])
async def get_five_new_comics(db: AsyncSession = Depends(get_db)):
    comics = await db.execute(select(m.Comic).order_by(desc(m.Comic.date_of_out)).limit(5)) 
    comics_list = comics.scalars().all()
    return comics_list


@router.get("/favorites/{nick}", response_model=List[pyd.ComicBase])
async def get_favorite_comics_by_nick(nick: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(m.User)
        .options(selectinload(m.User.favorite_comics))
        .where(m.User.nick == nick)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    sorted_comics = sorted(user.favorite_comics, key=lambda c: c.title.lower())

    return sorted_comics