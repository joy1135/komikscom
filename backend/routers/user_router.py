from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from database import get_db
import models as m
import pyd
from typing import List
import utils
from fastapi.security import OAuth2PasswordRequestForm
import auth

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post("/register", response_model=pyd.UserResponse)
async def register_user(
    user_data: pyd.UserCreate,
    db: AsyncSession = Depends(get_db)
):
    existing_email = await db.execute(
        select(m.User).where(m.User.email == user_data.email)
    )
    if existing_email.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Эта почта уже используется"
        )

    existing_nick = await db.execute(
        select(m.User).where(m.User.nick == user_data.nick)
    )
    if existing_nick.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Этот ник уже используется"
        )

    hashed_password = utils.hash_password(user_data.password)

    # Создание пользователя
    new_user = m.User(
        email=user_data.email,
        password=hashed_password,
        nick=user_data.nick,
        roleId= 2
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=pyd.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await db.execute(
        select(m.User).where(m.User.email == form_data.username)
    )
    user = user.scalar_one_or_none()
    
    if not user or not utils.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(
        data={"sub": user.email, "nick": user.nick}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=pyd.UserResponse)
async def read_users_me(current_user: m.User = Depends(auth.get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "nick": current_user.nick,
    }