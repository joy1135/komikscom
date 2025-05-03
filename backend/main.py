from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import comic_router, aftor_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(comic_router, prefix="/api", tags=["api"])
app.include_router(aftor_router, prefix="/api", tags=["api"])