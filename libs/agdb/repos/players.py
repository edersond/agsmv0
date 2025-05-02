from libs.agdb import AGDB_SCHEMA, AGDB_DSN
from libs import APP_GLOBALS
import asyncpg
from pydantic import validate_call
from libs.encryption import bcrypt_context
from agiota import get_agdb_pool



class AgdbPlayerRepository:
    """
    Repositorio de dados do jogador
    """
    @staticmethod
    @validate_call
    async def create_player_with_password(name: str, email: str, password: str):
        """
        Cria um jogador usando autenticacao propria (senha)
        
        Args:
            agdb (asyncpg.pool): Pool de conexao com o banco de dados
            name (str): Nome do jogador
            email (str): Email do jogador
            password (str): Senha do jogador
        """

        @validate_call
        async def insert_into_players(name: str, email: str):
            insert = f""" 
                INSERT INTO {AGDB_SCHEMA}.players (full_name, email)
                VALUES ($1, $2)
                RETURNING id, guid;
            """
            try:
                async with get_agdb_pool().acquire() as conn:
                    async with conn.transaction():
                        player = await conn.fetchrow(insert, name, email)
                return dict(player)
            except Exception as e:
                raise Exception(f"Error creating player: {e}")


        async def insert_into_auth_providers(newplayer_id: str, newplayer_guid: str, pwdhash: str):
            insert = f"""
                INSERT INTO {AGDB_SCHEMA}.auth_providers (user_id, provider, provider_user_id, password_hash)
                VALUES ($1, $2, $3, $4);
            """
            try:
                async with get_agdb_pool().acquire() as conn:
                    async with conn.transaction():
                        await conn.execute(insert, newplayer_id, 'local', newplayer_guid, pwdhash)
            except Exception as e:
                raise Exception(f"Error creating auth provider: {e}")
        
        newplayer = await insert_into_players(name, email)
        newplayer_id, newplayer_guid = newplayer['id'], newplayer['guid']
        await insert_into_auth_providers(newplayer_id, newplayer_guid, bcrypt_context.hash_password(password))
        return newplayer
        
        
