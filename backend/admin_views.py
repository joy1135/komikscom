from sqladmin import ModelView
import models as m

class UserAdmin(ModelView, model=m.User):
    column_list = [m.User.id, m.User.email, m.User.nick, m.User.roleId]
    column_searchable_list = [m.User.email, m.User.nick]
    column_editable_list = [m.User.roleId]
    name = "Пользователь"
    name_plural = "Пользователи"
    
class GenreAdmin(ModelView, model=m.Genre):
    column_list = [m.Genre.id, m.Genre.name]
    column_searchable_list = [m.Genre.name]
    name = "Жанр"
    name_plural = "Жанры"
    
class CommentAdmin(ModelView, model=m.Comment):
    column_list = [m.Comment.id, m.Comment.comment, m.Comment.userID, m.Comment.comicID]
    column_searchable_list = [m.Comment.comment]
    name = "Комментарий"
    name_plural = "Комментарии"
    
class ComicAdmin(ModelView, model=m.Comic):
    column_list = [m.Comic.id, m.Comic.title, m.Comic.website_recommendation]
    column_searchable_list = [m.Comic.title]
    column_editable_list = [m.Comic.website_recommendation]
    name = "Комикс"
    name_plural = "Комиксы"
    
class ComicGenreAdmin(ModelView, model=m.ComicGenre):
    column_list = [m.ComicGenre.comic_id, m.ComicGenre.genre_id]
    name = "Жанр Комикса"
    name_plural = "Жанры Комиксов"