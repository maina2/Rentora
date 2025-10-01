import asyncio
from sqlalchemy import text
from app.db.session import engine

async def test_tables():
    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT id, email, role FROM users"))
        print("Users:", result.fetchall())
        result = await connection.execute(text("SELECT id, user_id, name, phone FROM landlords"))
        print("Landlords:", result.fetchall())
        result = await connection.execute(text("SELECT id, user_id, name, phone FROM tenants"))
        print("Tenants:", result.fetchall())

if __name__ == "__main__":
    asyncio.run(test_tables())