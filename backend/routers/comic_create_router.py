from datetime import date
import os
import shutil
from fastapi import FastAPI, File, Form, HTTPException, Depends, APIRouter, UploadFile, Query
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
    prefix="/create",
    tags=["create"],
)

FILES_ROOT = "files"
COMICS_ROOT = os.path.join(FILES_ROOT, "comics")

@router.post("/comics/")
async def create_comic(
    title: str = Form(...),
    desc: str = Form(None),
    poster: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: m.User = Depends(get_current_user),
):

    existing = await db.execute(select(m.Comic).where(m.Comic.title == title))
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="Комикс с таким названием уже существует")

    safe_folder_name = title.replace(" ", "_")

    comic_root = os.path.join(COMICS_ROOT, safe_folder_name)
    poster_folder = os.path.join(comic_root, "poster")
    comic_folder = os.path.join(comic_root, "comic")
    os.makedirs(poster_folder, exist_ok=True)
    os.makedirs(comic_folder, exist_ok=True)

    # Сохраняем постер
    poster_filename = f"{safe_folder_name}_poster.jpg"
    poster_path = os.path.join(poster_folder, poster_filename)
    with open(poster_path, "wb") as f:
        shutil.copyfileobj(poster.file, f)

    relative_poster_path = os.path.relpath(poster_path, FILES_ROOT).replace("\\", "/")

    new_comic = m.Comic(
        title=title,
        desc=desc,
        date_of_out=date.today(),
        website_recommendation=False,
        img=relative_poster_path,
        userID=current_user.id,
    )
    db.add(new_comic)
    await db.commit()
    await db.refresh(new_comic)

    return {"id": new_comic.id, "title": new_comic.title}
