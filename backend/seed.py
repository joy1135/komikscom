from sqlalchemy.orm import Session
from database import engine
import models as m

m.Base.metadata.drop_all(bind=engine)
m.Base.metadata.create_all(bind=engine)

with Session(bind=engine) as session:
    role1 = m.Role(name="Admin")
    role2 = m.Role(name="User")
    session.add_all([role1, role2])
    session.flush()

    user1 = m.User(
        email="user1@example.com",
        nick="user1",
        password="password1",
        roleId=role1.id
    )
    user2 = m.User(
        email="user2@example.com",
        nick="user2",
        password="password2",
        roleId=role2.id
    )
    session.add_all([user1, user2])
    session.flush()

    genre1 = m.Genre(name="Fantasy")
    genre2 = m.Genre(name="Adventure")
    session.add_all([genre1, genre2])
    session.flush()

    comic1 = m.Comic(
        title="Комикс 1",
        image="image1.jpg",
        date_of_out="2025-04-28",
        userID=user1.id
    )
    comic2 = m.Comic(
        title="Комикс 2",
        image="image2.jpg",
        date_of_out="2025-05-01",
        userID=user2.id
    )
    session.add_all([comic1, comic2])
    session.flush() 

    comic1.genres.append(genre1)
    comic2.genres.append(genre2)

    rating1 = m.Rating(
        user_id=user1.id,
        comic_id=comic1.id,
        value=8
    )
    rating2 = m.Rating(
        user_id=user2.id,
        comic_id=comic1.id,
        value=9
    )
    session.add_all([rating1, rating2])

    comment1 = m.Comment(
        userID=user1.id,
        comicID=comic1.id,
        comment="Отличный комикс!"
    )
    comment2 = m.Comment(
        userID=user2.id,
        comicID=comic2.id,
        comment="Интересная история."
    )
    session.add_all([comment1, comment2])
    
    session.commit()