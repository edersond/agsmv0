#
"""
agdb - Agiota Database Library
"""
import asyncpg
import asyncio
import os
from libs import APP_GLOBALS
AGDB_DSN = lambda: f"postgresql://{os.getenv('AGDB_USER', 'default_user')}:{os.getenv('AGDB_PWD', 'default_password')}@34.9.124.93:5432/{os.getenv('AGDB_DB', 'default_db')}"
AGDB_SCHEMA = 'agsim0'

async def create_pool():
    """
    Create a connection pool to the database
    """
    pool = await asyncpg.create_pool(dsn=AGDB_DSN(), min_size=1, max_size=10, timeout=60,max_queries=50000, max_inactive_connection_lifetime=300, command_timeout=60, statement_cache_size=1000)
    return pool

async def close_pool(pool):
    """
    Close the connection pool
    """
    await pool.close()

async def migrate_ddl():
    """
    Migrate the database schema
    """
    conn = await asyncpg.connect(dsn=AGDB_DSN())
    
    #create schema
    await conn.execute(f"""
        CREATE SCHEMA IF NOT EXISTS {AGDB_SCHEMA};
    """)
    
    #create table players
    await conn.execute(
        f"""
            CREATE TABLE IF NOT EXISTS {AGDB_SCHEMA}.players (
                id SERIAL PRIMARY KEY,
                guid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid();
                email TEXT UNIQUE NOT NULL,
                full_name TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)


    # Criação da tabela de provedores de autenticação
    await conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {AGDB_SCHEMA}.auth_providers (
            id SERIAL PRIMARY KEY,
            guid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid();
            user_id INTEGER NOT NULL REFERENCES {AGDB_SCHEMA}.players(id) ON DELETE CASCADE,
            provider TEXT NOT NULL, -- 'local', 'google', 'github'
            provider_user_id TEXT, -- ID do Google ou GitHub
            password_hash TEXT, -- Só usado no 'local'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (provider, provider_user_id) -- Evita duplicidade
        );
    """)
    await conn.close()

