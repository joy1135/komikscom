import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import *
from admin import setup_admin
from database import engine, Base
from starlette.middleware.sessions import SessionMiddleware
from config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_admin(app)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
app.mount(
    "/comics",
    StaticFiles(directory=os.path.join("files", "comics")),
    name="comics"
)

app.include_router(comic_router, prefix="/api", tags=["api"])
app.include_router(aftor_router, prefix="/api", tags=["api"])
app.include_router(user_router, prefix="/api", tags=["api"])
app.include_router(genre_router, prefix="/api", tags=["api"])
app.include_router(comic_create_router, prefix="/api", tags=["api"])
app.include_router(comment_router, prefix="/api", tags=["api"])