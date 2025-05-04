import asyncpg, asyncio, os
from dotenv import load_dotenv ; load_dotenv('.env')
from contextlib import asynccontextmanager
from typing_extensions import Optional, Dict, Any


async def create_pool() -> asyncpg.Pool:
    """
    Create a connection pool to the PostgreSQL database.
    """
    return await asyncpg.create_pool(
        host=os.getenv("PGDB_HOST"),
        port=int(os.getenv("PGDB_PORT")),
        user=os.getenv("PGDB_USER"),
        password=os.getenv("PGDB_PASSWORD"),
        database=os.getenv("PGDB_DATABASE"),
        min_size=1,
        max_size=10,
        timeout=60
    )

