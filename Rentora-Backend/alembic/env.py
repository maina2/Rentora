# alembic/env.py
import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context
from app.db.base import Base
from app.core.config import settings


config = context.config

database_url = settings.DATABASE_URL
if "?" in database_url:
    database_url = database_url.split("?")[0]

async_database_url = f"postgresql+asyncpg://{database_url[len('postgresql://'):]}"
config.set_main_option("sqlalchemy.url", async_database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=async_database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode (async)."""
    connectable: AsyncEngine = create_async_engine(async_database_url, echo=True)

    async with connectable.connect() as connection:
        # Start a transaction explicitly
        trans = await connection.begin()
        try:
            await connection.run_sync(
                lambda sync_conn: context.configure(
                    connection=sync_conn,
                    target_metadata=target_metadata,
                )
            )
            await connection.run_sync(lambda sync_conn: context.run_migrations())
            # Commit the transaction
            await trans.commit()
        except Exception:
            # Rollback on error
            await trans.rollback()
            raise

        
def run_migrations():
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())


run_migrations()
