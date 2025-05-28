# admin_auth.py
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from sqlalchemy import select
from passlib.context import CryptContext
from database import AsyncSessionLocal
from config import settings
import models as m

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AdminAuth(AuthenticationBackend):
    def __init__(self):
        super().__init__(secret_key=settings.SECRET_KEY)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = form.get("username")
        password = form.get("password")

        async with AsyncSessionLocal() as session:
            result = await session.execute(select(m.User).where(m.User.email == email))
            user = result.scalar_one_or_none()

            if not user or not pwd_context.verify(password, user.password) or user.roleId != 1:
                return False

            request.session.update({"admin": True})
            return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("admin") is True
