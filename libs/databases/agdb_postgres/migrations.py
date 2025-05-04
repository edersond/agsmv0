import asyncpg, asyncio
from contextlib import asynccontextmanager
from typing_extensions import Optional, Dict, Any
from libs.databases.agdb_postgres.pool import create_pool
from rich import print


DEFAULT_SCHEMA = "agdb0"
async def create_schemas(pool: Optional[asyncpg.Pool] = None) -> None:
    """
    Create the schemas in the PostgreSQL database.
    """
    async with pool.acquire() as connection:
        try:
            await connection.execute(f"CREATE SCHEMA IF NOT EXISTS {DEFAULT_SCHEMA};")
        except asyncpg.exceptions.DuplicateSchemaError:
            print("[bold red]Schema already exists, skipping creation.[/]")
    return None

async def create_tables(pool: Optional[asyncpg.Pool] = None) -> None:
    """
    Create the tables in the PostgreSQL database.
    """
    async def ct_players():
        async with pool.acquire() as connection:
            await connection.execute(f"""
                CREATE TABLE IF NOT EXISTS {DEFAULT_SCHEMA}.players (
                	pk bigserial NOT NULL,
                    id uuid NOT NULL,
                    "name" varchar(255) NOT NULL,
                    email varchar(255) NOT NULL,
                    is_active bool DEFAULT true NOT NULL,
                    is_banned bool DEFAULT false NOT NULL,
                    is_deleted bool DEFAULT false NOT NULL,
                    is_verified bool DEFAULT false NOT NULL,
                    is_premium bool DEFAULT false NOT NULL,
                    "level" int4 NOT NULL,
                    bankroll int4 NOT NULL,
                    created_at timestamp DEFAULT now() NOT NULL,
                    updated_at timestamp DEFAULT now() NOT NULL,
                    CONSTRAINT players_email_unique UNIQUE (email),
                    CONSTRAINT players_id_unique UNIQUE (id),
                    CONSTRAINT players_pkey PRIMARY KEY (pk)
                );
                CREATE INDEX idx_players_bankroll ON {DEFAULT_SCHEMA}.players USING btree (bankroll);
                CREATE INDEX idx_players_email ON {DEFAULT_SCHEMA}.players USING btree (email);
                CREATE INDEX idx_players_id ON {DEFAULT_SCHEMA}.players USING btree (id);
                CREATE INDEX idx_players_is_active ON {DEFAULT_SCHEMA}.players USING btree (is_active);
                CREATE INDEX idx_players_level ON {DEFAULT_SCHEMA}.players USING btree (level);
                );
                """)
            

async def main():
    pool = await create_pool()
    await create_schemas(pool)
    await create_tables(pool)

asyncio.run(main())

