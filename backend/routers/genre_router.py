from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, APIRouter, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc
from sqlalchemy.orm import selectinload, joinedload
import models as m
from typing import List
import pyd

router = APIRouter(
    prefix="/genre",
    tags=["genre"],
)

@router.get("/", response_model=List[pyd.GenreBase])
async def get_all_genre(db: AsyncSession = Depends(get_db)):
    genres = await db.execute(select(m.Genre).order_by(asc(m.Genre.name))) 
    genres_list = genres.scalars().all()
    return genres_list
