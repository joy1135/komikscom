from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker
from config import settings

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# Создание асинхронного движка
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # для проверки соединения с базой
    echo=True  # для логирования SQL запросов
)

# Асинхронная фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# Определение базового класса для моделей
Base = declarative_base()

# Асинхронный генератор для работы с базой данных
async def get_db():
    async with AsyncSessionLocal() as db:  # Контекстный менеджер автоматически закроет сессию
        yield db
