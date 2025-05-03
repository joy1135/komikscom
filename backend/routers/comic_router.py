from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, APIRouter, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload, joinedload
import models as m
from typing import List
import pyd

router = APIRouter(
    prefix="/comic",
    tags=["comic"],
)

@router.get("/", response_model=List[pyd.ComicBase])
async def get_all_comics(db: AsyncSession = Depends(get_db)):
    comics = await db.execute(select(m.Comic)) 
    comics_list = comics.scalars().all()
    return comics_list

@router.get("/full_info", response_model=List[pyd.ComicResponse])
async def get_all_info_comics(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(m.Comic).options(
            selectinload(m.Comic.genres),
            joinedload(m.Comic.user).options( 
                joinedload(m.User.role)
            )
        )
    )
    comics = result.unique().scalars().all()
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