from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Annotated
from config import settings
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
import models as m

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_current_user(
    request: Request,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> m.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    ) 
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        nick: str = payload.get("nick")
        id: int = payload.get("id")
        role: int = payload.get("role")
        if not email:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e
    
    result = await db.execute(select(m.User).where(m.User.email == email))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
        
    return user