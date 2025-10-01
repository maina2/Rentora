from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from decouple import config
from typing import AsyncGenerator


base_url = config("DATABASE_URL")

if "?" in base_url:
    base_url = base_url.split("?")[0]


DATABASE_URL = f"postgresql+asyncpg://{base_url[len('postgresql://'):]}"  

engine = create_async_engine(DATABASE_URL, echo=True)


AsyncSessionFactory = async_sessionmaker(
    engine, expire_on_commit=False, autoflush=False, class_=AsyncSession
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        yield session