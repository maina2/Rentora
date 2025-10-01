# drop_alembic_version.py
import asyncio
from sqlalchemy import text
from app.db.session import engine

async def drop_alembic_version():
    async with engine.connect() as connection:
        await connection.execute(text("DROP TABLE IF EXISTS alembic_version"))
        await connection.commit()
        print("Dropped alembic_version table")

if __name__ == "__main__":
    asyncio.run(drop_alembic_version())