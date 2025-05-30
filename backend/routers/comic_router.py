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
    prefix="/comic",
    tags=["comic"],
)

@router.get("/", response_model=List[pyd.ComicBase])
async def get_all_comics(db: AsyncSession = Depends(get_db)):
    comics = await db.execute(select(m.Comic)) 
    comics_list = comics.scalars().all()
    return comics_list


@router.get("/comics", response_model=List[pyd.ComicBase])
async def get_comics(
    genres: List[int] = Query(default=[]),
    min_rating: Optional[float] = Query(default=None, ge=0.0, le=10.0),
    sort: Optional[str] = Query(default="avg_rating", enum=["asc", "avg_rating", "popular"]),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=30),  
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
        stmt = stmt.order_by(desc(rating_count), nullslast(desc(avg_rating)))
    else:  
        stmt = stmt.order_by(nullslast(desc(avg_rating))) 
    stmt = stmt.options(selectinload(m.Comic.genres))
    offset = (page - 1) * limit
    stmt = stmt.offset(offset).limit(limit)

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
    
@router.get("/search", response_model=List[pyd.ComicBase])
async def search_comics_by_title(
    title: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(m.Comic).options(selectinload(m.Comic.genres))

    if title:
        stmt = stmt.where(m.Comic.title.ilike(f"%{title}%"))

    result = await db.execute(stmt)
    comics = result.scalars().all()
    return comics

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

from sqlalchemy import func

@router.get("/comics/{comic_id}", response_model=pyd.ComicResponse)
async def get_comic_by_id(
    comic_id: int,
    db: AsyncSession = Depends(get_db),
):
    stmt = (
    select(m.Comic)
    .where(m.Comic.id == comic_id)
    .options(
        selectinload(m.Comic.user),
        selectinload(m.Comic.genres),
        selectinload(m.Comic.volumes)
        .selectinload(m.Volume.chapters)
        .options(noload(m.Chapter.pages)),
    )
    )
    result = await db.execute(stmt)
    comic = result.scalars().first()

    if not comic:
        raise HTTPException(status_code=404, detail="Комикс не найден")

    rating_stmt = select(func.avg(m.Rating.value)).where(m.Rating.comic_id == comic_id)
    rating_result = await db.execute(rating_stmt)
    average_rating = rating_result.scalar()

    comic.average_rating = average_rating

    return comic

@router.get("/chapters/{chapter_id}", response_model=list[pyd.PageResponse])
async def get_pages_by_chapter_id(
    chapter_id: int,
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(m.Page)
        .where(m.Page.chapter_id == chapter_id)
        .order_by(m.Page.number)
    )
    result = await db.execute(stmt)
    pages = result.scalars().all()

    if not pages:
        raise HTTPException(status_code=404, detail="Страница не найдена")

    return pages

@router.post("/{comic_id}/favorite")
async def add_comic_to_favorites(
    comic_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: m.User = Depends(get_current_user),
):
    stmt = pg_insert(m.user_favorite_comics).values(user_id=current_user.id, comic_id=comic_id)
    stmt = stmt.on_conflict_do_nothing(index_elements=["user_id", "comic_id"])
    await db.execute(stmt)
    await db.commit()
    return {"message": "Комикс добавлен в любимое"}

@router.delete("/{comic_id}/del_favorite")
async def remove_comic_from_favorites(
    comic_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: m.User = Depends(get_current_user),
):
    stmt = delete(m.user_favorite_comics).where(
        m.user_favorite_comics.c.user_id == current_user.id,
        m.user_favorite_comics.c.comic_id == comic_id
    )
    await db.execute(stmt)
    await db.commit()
    return {"message": "Комикс удален из любимого"}

@router.get("/{comic_id}/is_favorite", response_model=bool)
async def is_comic_favorite(
    comic_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: m.User = Depends(get_current_user),
):
    stmt = select(m.user_favorite_comics).where(
        m.user_favorite_comics.c.user_id == current_user.id,
        m.user_favorite_comics.c.comic_id == comic_id
    )
    result = await db.execute(stmt)
    return result.first() is not None