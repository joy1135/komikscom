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

@router.post("/comics/{comic_id}/volumes")
async def create_volume(
    comic_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: m.User = Depends(get_current_user),
):
    result = await db.execute(select(m.Comic).where(m.Comic.id == comic_id))
    comic = result.scalar_one_or_none()
    if not comic:
        raise HTTPException(status_code=404, detail="Комикс не найден")

    next_number = len(comic.volumes) + 1

    volume = m.Volume(number=next_number, comic_id=comic_id)
    db.add(volume)
    await db.commit()
    await db.refresh(volume)

    comic_folder = os.path.join(COMICS_ROOT, comic.title.replace(" ", "_"), "comic")
    volume_folder = os.path.join(comic_folder, f"vl{volume.number}")
    os.makedirs(volume_folder, exist_ok=True)

    return {"id": volume.id, "number": volume.number}

@router.post("/volumes/{volume_id}/chapters")
async def create_chapter(
    volume_id: int,
    title: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: m.User = Depends(get_current_user),
):
    result = await db.execute(select(m.Volume).options(selectinload(m.Volume.comic)).where(m.Volume.id == volume_id))
    volume = result.scalar_one_or_none()
    if not volume:
        raise HTTPException(status_code=404, detail="Том не найден")

    next_number = len(volume.chapters) + 1

    chapter = m.Chapter(number=next_number, title=title, volume_id=volume_id)
    db.add(chapter)
    await db.commit()
    await db.refresh(chapter)

    comic_title_safe = volume.comic.title.replace(" ", "_")
    chapter_folder = os.path.join(
        COMICS_ROOT, comic_title_safe, "comic", f"vl{volume.number}", f"ch{chapter.number}"
    )
    os.makedirs(chapter_folder, exist_ok=True)

    return {"id": chapter.id, "number": chapter.number, "title": chapter.title}

@router.delete("/volumes/{volume_id}")
async def delete_volume(
    volume_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: m.User = Depends(get_current_user),
):
    result = await db.execute(select(m.Volume).where(m.Volume.id == volume_id).options(
        selectinload(m.Volume.comic),
        selectinload(m.Volume.chapters),
    ))
    volume = result.scalar_one_or_none()
    if not volume:
        raise HTTPException(status_code=404, detail="Том не найден")

    comic_title_safe = volume.comic.title.replace(" ", "_")
    volume_folder = os.path.join(
        COMICS_ROOT,
        comic_title_safe,
        "comic",
        f"vl{volume.number}",
    )
    if os.path.exists(volume_folder):
        shutil.rmtree(volume_folder)

    await db.delete(volume)
    await db.commit()

    return {"detail": "Том удалён"}


@router.delete("/chapters/{chapter_id}")
async def delete_chapter(
    chapter_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: m.User = Depends(get_current_user),
):
    result = await db.execute(select(m.Chapter).where(m.Chapter.id == chapter_id).options(
        selectinload(m.Chapter.pages),
        selectinload(m.Chapter.volume).selectinload(m.Volume.comic),
    ))
    chapter = result.scalar_one_or_none()
    if not chapter:
        raise HTTPException(status_code=404, detail="Глава не найдена")

    comic_title_safe = chapter.volume.comic.title.replace(" ", "_")
    chapter_folder = os.path.join(
        COMICS_ROOT,
        comic_title_safe,
        "comic",
        f"vl{chapter.volume.number}",
        f"ch{chapter.number}",
    )
    if os.path.exists(chapter_folder):
        shutil.rmtree(chapter_folder)

    await db.delete(chapter)
    await db.commit()

    return {"detail": "Глава удалена"}



@router.post("/chapters/{chapter_id}/pages")
async def upload_pages_to_chapter(
    chapter_id: int,
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: m.User = Depends(get_current_user),
):
    result = await db.execute(
        select(m.Chapter)
        .options(selectinload(m.Chapter.volume).selectinload(m.Volume.comic))
        .where(m.Chapter.id == chapter_id)
    )
    chapter = result.scalar_one_or_none()
    if not chapter:
        raise HTTPException(status_code=404, detail="Глава не найдена")

    comic_title_safe = chapter.volume.comic.title.replace(" ", "_")
    chapter_folder = os.path.join(
        COMICS_ROOT,
        comic_title_safe,
        "comic",
        f"vl{chapter.volume.number}",
        f"ch{chapter.number}",
    )
    os.makedirs(chapter_folder, exist_ok=True)

    result = await db.execute(
        select(func.max(m.Page.number)).where(m.Page.chapter_id == chapter.id)
    )
    max_page_number = result.scalar() or 0

    created_pages = []

    for i, file in enumerate(files, start=1):
        page_number = max_page_number + i

        extension = os.path.splitext(file.filename)[1]
        filename = f"{page_number}{extension}"
        filepath = os.path.join(chapter_folder, filename)

        with open(filepath, "wb") as f:
            content = await file.read()
            f.write(content)

        relative_path = os.path.relpath(filepath, FILES_ROOT).replace("\\", "/")
        page = m.Page(
            number=page_number,
            image_url=relative_path,
            chapter_id=chapter.id
        )
        db.add(page)
        created_pages.append(page_number)

    await db.commit()

    return {"detail": f"{len(created_pages)} страниц добавлено", "pages": created_pages}


@router.delete("/pages/{page_id}")
async def delete_page(
    page_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: m.User = Depends(get_current_user),
):
    result = await db.execute(select(m.Page).where(m.Page.id == page_id).options(selectinload(m.Page.chapter)))
    page = result.scalar_one_or_none()
    if not page:
        raise HTTPException(status_code=404, detail="Страница не найдена")

    # Удаляем файл
    file_path = os.path.join(FILES_ROOT, page.image_url)
    if os.path.exists(file_path):
        os.remove(file_path)

    await db.delete(page)
    await db.commit()

    folder_path = os.path.dirname(file_path)
    try:
        os.rmdir(folder_path)  
    except OSError:
        pass  

    return {"detail": "Страница удалена"}
