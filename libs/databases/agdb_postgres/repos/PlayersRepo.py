import asyncpg
from models import PlayerModels

class Insert:
    @staticmethod
    async def new_player(pool: asyncpg.Pool, player: PlayerModels.NewPlayer):
        """
        Insert a new player into the database
        """
        try:
            async with pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(
                        """
                            INSERT INTO agdb0.players (id, name, email, is_active, is_banned, is_deleted, is_verified, is_premium, level, bankroll, created_at, updated_at) 
                            VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, now(), now());
                        """,
                        player.id,
                        player.name,
                        player.email,
                        player.is_active,
                        player.is_banned,
                        player.is_deleted,
                        player.is_verified,
                        player.is_premium,
                        player.level,
                        player.bankroll
                    )
                return True
        except asyncpg.exceptions.UniqueViolationError as e:
            raise Exception(f"Player with id {player.id} already exists") from e
        except asyncpg.exceptions.ForeignKeyViolationError as e:
            raise Exception(f"Foreign key violation: {e}") from e
        except asyncpg.exceptions.CheckViolationError as e:
            raise Exception(f"Check constraint violation: {e}") from e
        except asyncpg.exceptions.PostgresError as e:
            raise Exception(f"Postgres error: {e}") from e
        except Exception as e:
            raise Exception(f"Error inserting player: {e}") from e
        

class Fetch:
    @staticmethod
    async def player_by_id(pool: asyncpg.Pool, player_id: str):
        """
        Get a player by id
        """
        try:
            async with pool.acquire() as conn:
                player = await conn.fetchrow(
                    """
                        SELECT * FROM agdb0.players WHERE id = $1;
                    """,
                    player_id
                )
                if player is None:
                    raise Exception(f"Player with id {player_id} not found")
                return PlayerModels.Player(**player)
        except asyncpg.exceptions.PostgresError as e:
            raise Exception(f"Postgres error: {e}") from e
        except Exception as e:
            raise Exception(f"Error getting player: {e}") from e       
            