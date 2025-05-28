import asyncio
import os
import shutil
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from database import engine
import models as m
import bcrypt

FILES_ROOT = "files"
SEED_PAGES_FOLDER = os.path.join(FILES_ROOT, "seed/test")
SEED_POSTER_PATH = os.path.join(FILES_ROOT, "seed/posters", "1.jpg")
COMICS_ROOT = os.path.join(FILES_ROOT, "comics")
VALID_IMAGE_EXTENSIONS = [".jpg", ".png"]
salt = bcrypt.gensalt()

async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(m.Base.metadata.drop_all)
        await conn.run_sync(m.Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Roles
        admin_role = m.Role(name="Admin")
        user_role = m.Role(name="User")
        aftor_role = m.Role(name="Aftor")
        session.add_all([admin_role, user_role, aftor_role])
        await session.flush()

        # Users
        admin_user = m.User(
            email="admin@example.com",
            nick="admin",
            password=(bcrypt.hashpw("admin123".encode('utf-8'), salt)).decode('utf-8'),
            roleId=admin_role.id
        )
        regular_user = m.User(
            email="user@example.com",
            nick="user",
            password=(bcrypt.hashpw("user123".encode('utf-8'), salt)).decode('utf-8'),
            roleId=user_role.id
        )
        aftor_user = m.User(
            email="aftor@example.com",
            nick="aftor",
            password=(bcrypt.hashpw("aftor123".encode('utf-8'), salt)).decode('utf-8'),
            roleId=aftor_role.id
        )
        session.add_all([admin_user, regular_user, aftor_user])
        await session.flush()

        # Genres
        fantasy = m.Genre(name="Fantasy")
        adventure = m.Genre(name="Adventure")
        scifi = m.Genre(name="Sci-Fi")
        session.add_all([fantasy, adventure, scifi])
        await session.flush()

        # Comics
        comic1 = m.Comic(
            title="Комикс1",
            date_of_out=date(2023, 1, 15),
            userID=admin_user.id,
            website_recommendation=True,
            img=""
        )
        comic2 = m.Comic(
            title="Комикс2",
            date_of_out=date(2023, 2, 20),
            userID=aftor_user.id,
            website_recommendation=False,
            img=""
        )
        session.add_all([comic1, comic2])
        await session.flush()

        # Add genres to comics
        session.add_all([
            m.ComicGenre(comic_id=comic1.id, genre_id=fantasy.id),
            m.ComicGenre(comic_id=comic1.id, genre_id=adventure.id),
            m.ComicGenre(comic_id=comic2.id, genre_id=scifi.id)
        ])
        await session.flush()

        # Add posters
        for comic in [comic1, comic2]:
            poster_folder = os.path.join(COMICS_ROOT, comic.title, "poster")
            os.makedirs(poster_folder, exist_ok=True)

            poster_filename = f"{comic.title}_poster.jpg"
            dest_poster_path = os.path.join(poster_folder, poster_filename)

            if os.path.exists(SEED_POSTER_PATH):
                shutil.copyfile(SEED_POSTER_PATH, dest_poster_path)
                relative_img_path = os.path.relpath(dest_poster_path, FILES_ROOT).replace("\\", "/")
                comic.img = relative_img_path
            else:
                comic.img = ""

        # Add volumes, chapters, pages
        for comic in [comic1, comic2]:
            volume = m.Volume(number=1, comic_id=comic.id)
            session.add(volume)
            await session.flush()

            chapter = m.Chapter(number=1, title=None, volume_id=volume.id)
            session.add(chapter)
            await session.flush()

            target_chapter_folder = os.path.join(COMICS_ROOT, comic.title, "comic", "vl1", "ch1")
            os.makedirs(target_chapter_folder, exist_ok=True)

            for file_name in sorted(os.listdir(SEED_PAGES_FOLDER)):
                if not any(file_name.lower().endswith(ext) for ext in VALID_IMAGE_EXTENSIONS):
                    continue
                try:
                    page_number = int(os.path.splitext(file_name)[0])
                except ValueError:
                    continue

                source_path = os.path.join(SEED_PAGES_FOLDER, file_name)
                dest_path = os.path.join(target_chapter_folder, file_name)
                shutil.copyfile(source_path, dest_path)

                relative_path = os.path.relpath(dest_path, FILES_ROOT).replace("\\", "/")
                page = m.Page(
                    number=page_number,
                    image_url=relative_path,
                    chapter_id=chapter.id
                )
                session.add(page)

        # Ratings
        ratings = [
            m.Rating(user_id=admin_user.id, comic_id=comic1.id, value=9),
            m.Rating(user_id=regular_user.id, comic_id=comic1.id, value=8),
            m.Rating(user_id=regular_user.id, comic_id=comic2.id, value=7)
        ]
        session.add_all(ratings)

        # Comments
        comments = [
            m.Comment(userID=admin_user.id, comicID=comic1.id, comment="Отличный комикс! Рекомендую!"),
            m.Comment(userID=regular_user.id, comicID=comic2.id, comment="Интересный сюжет, но концовка слабовата")
        ]
        session.add_all(comments)

        # Favorites
        await session.execute(m.user_favorite_comics.insert().values(user_id=aftor_user.id, comic_id=comic1.id))

        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed())
