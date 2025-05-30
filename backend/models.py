from sqlalchemy import Date, Column, ForeignKey, Integer, String, UniqueConstraint, Boolean, Table
from sqlalchemy.orm import relationship
from database import Base

user_favorite_comics = Table(
    "user_favorite_comics",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("comic_id", Integer, ForeignKey("comics.id", ondelete="CASCADE"), primary_key=True)
)

class ComicGenre(Base):
    __tablename__ = "comic_genres"
    comic_id = Column(Integer, ForeignKey("comics.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), primary_key=True)

class Comic(Base):
    __tablename__ = "comics"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True, nullable=False)
    desc = Column(String(255), nullable=True)
    date_of_out = Column(Date, nullable=False)
    userID = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    website_recommendation = Column(Boolean, nullable=False)
    img = Column(String(255), nullable=False)
    user = relationship("User", backref="comics")
    genres = relationship("Genre", secondary="comic_genres", backref="comics", lazy='selectin')
    volumes = relationship("Volume", back_populates="comic", cascade="all, delete-orphan", lazy="selectin")
    favorited_by_users = relationship(
        "User",
        secondary="user_favorite_comics",
        back_populates="favorite_comics",
        lazy="selectin"
    )
    def __str__(self):
        return self.title

class Volume(Base):
    __tablename__ = "volumes"
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    comic_id = Column(Integer, ForeignKey("comics.id"), nullable=False)

    comic = relationship("Comic", back_populates="volumes")
    chapters = relationship("Chapter", back_populates="volume", cascade="all, delete-orphan", lazy="selectin")
    
class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=True)
    volume_id = Column(Integer, ForeignKey("volumes.id"), nullable=False)

    volume = relationship("Volume", back_populates="chapters")
    pages = relationship("Page", back_populates="chapter", cascade="all, delete-orphan", lazy="selectin")
    
class Page(Base):
    __tablename__ = "pages"
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    image_url = Column(String(255), nullable=False)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False)

    chapter = relationship("Chapter", back_populates="pages")

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    
    def __str__(self):
        return self.name

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    nick = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False) 
    roleId = Column(Integer, ForeignKey('roles.id'), nullable=False)

    role = relationship("Role", backref="users")

    favorite_comics = relationship(
        "Comic",
        secondary="user_favorite_comics",
        back_populates="favorited_by_users",
        lazy="selectin"
    )
    
    def __str__(self):
        return self.email

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('users.id'), nullable=False)
    comment = Column(String(255), nullable=False) 
    comicID = Column(Integer, ForeignKey('comics.id'), nullable=False)

    user = relationship("User", backref="comments")
    comic = relationship("Comic", backref="comments")
    
    def __str__(self):
        return self.comment

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    
    def __str__(self):
        return self.name

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
    
    def __str__(self):
        return str(self.value)
  