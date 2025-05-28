from sqladmin import Admin
from database import engine
from admin_auth import AdminAuth
from models import User, Genre, Comment, Comic, ComicGenre

from admin_views import UserAdmin, GenreAdmin, CommentAdmin, ComicAdmin, ComicGenreAdmin

def setup_admin(app):
    admin = Admin(app, engine, authentication_backend=AdminAuth())
    admin.add_view(UserAdmin)
    admin.add_view(GenreAdmin)
    admin.add_view(CommentAdmin)
    admin.add_view(ComicAdmin)
    admin.add_view(ComicGenreAdmin)