import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from database import engine
import models as m
from datetime import date

async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(m.Base.metadata.drop_all)
        await conn.run_sync(m.Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Создаем роли
        admin_role = m.Role(name="Admin")
        user_role = m.Role(name="User")
        aftor_role = m.Role(name = "Aftor")
        session.add_all([admin_role, user_role, aftor_role])
        await session.flush()

        admin_user = m.User(
            email="admin@example.com",
            nick="admin",
            password="admin123",
            roleId=admin_role.id
        )
        regular_user = m.User(
            email="user@example.com",
            nick="user",
            password="user123",
            roleId=user_role.id
        )
        aftor_user = m.User(
            email="aftor@example.com",
            nick="aftor",
            password="aftor123",
            roleId=aftor_role.id
        )
        session.add_all([admin_user, regular_user, aftor_user])
        await session.flush()

        # Создаем жанры
        fantasy = m.Genre(name="Fantasy")
        adventure = m.Genre(name="Adventure")
        scifi = m.Genre(name="Sci-Fi")
        session.add_all([fantasy, adventure, scifi])
        await session.flush()

        # Создаем комиксы
        comic1 = m.Comic(
            title="Комикс 1",
            image="comic1.jpg",
            date_of_out=date(2023, 1, 15),
            userID=admin_user.id,
            website_recommendation = True
        )
        comic2 = m.Comic(
            title="Комикс 2",
            image="comic2.jpg",
            date_of_out=date(2023, 2, 20),
            userID=aftor_user.id,
            website_recommendation = False
        )
        session.add_all([comic1, comic2])
        await session.flush()

        # Связываем комиксы с жанрами через ассоциативную таблицу
        session.add_all([
            m.ComicGenre(comic_id=comic1.id, genre_id=fantasy.id),
            m.ComicGenre(comic_id=comic1.id, genre_id=adventure.id),
            m.ComicGenre(comic_id=comic2.id, genre_id=scifi.id)
        ])
        await session.flush()

        # Создаем оценки
        ratings = [
            m.Rating(user_id=admin_user.id, comic_id=comic1.id, value=9),
            m.Rating(user_id=regular_user.id, comic_id=comic1.id, value=8),
            m.Rating(user_id=regular_user.id, comic_id=comic2.id, value=7)
        ]
        session.add_all(ratings)

        # Создаем комментарии
        comments = [
            m.Comment(
                userID=admin_user.id,
                comicID=comic1.id,
                comment="Отличный комикс! Рекомендую!"
            ),
            m.Comment(
                userID=regular_user.id,
                comicID=comic2.id,
                comment="Интересный сюжет, но концовка слабовата"
            )
        ]
        session.add_all(comments)

        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed())