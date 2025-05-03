from sqlalchemy import Date, Column, ForeignKey, Integer, String, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from database import Base

class ComicGenre(Base):
    __tablename__ = "comic_genres"
    comic_id = Column(Integer, ForeignKey("comics.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), primary_key=True)

class Comic(Base):
    __tablename__ = "comics"
    id = Column(Integer, primary_key=True)
    image = Column(String(255), nullable=False)
    title = Column(String(255), unique=True, nullable=False)
    date_of_out = Column(Date, nullable=False)
    userID = Column(Integer, ForeignKey("users.id"), nullable=False)
    website_recommendation = Column(Boolean, nullable = False)

    user = relationship("User", backref="comics")
    genres = relationship("Genre", secondary="comic_genres", backref="comics", lazy='selectin')

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    nick = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # Убрал unique=True
    roleId = Column(Integer, ForeignKey('roles.id'), nullable=False)

    role = relationship("Role", backref="users")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('users.id'), nullable=False)
    comment = Column(String(255), nullable=False)  # Убрал unique=True
    comicID = Column(Integer, ForeignKey('comics.id'), nullable=False)

    user = relationship("User", backref="comments")
    comic = relationship("Comic", backref="comments")

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Убрал unique=True
    comic_id = Column(Integer, ForeignKey('comics.id'), nullable=False)
    value = Column(Integer, nullable=False)

    user = relationship("User", backref="ratings")
    comic = relationship("Comic", backref="ratings")

    __table_args__ = (
        UniqueConstraint('user_id', 'comic_id', name='_user_comic_uc'),
    )