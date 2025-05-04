from pydantic import BaseModel, Field, validate_call
from typing_extensions import Optional, Dict, Any, Annotated, Union
import uuid

def postgres_uuid2str(uuid: uuid.UUID) -> str:
    """
    Convert a UUID to a string
    """
    return str(uuid)


class NewPlayer(BaseModel):
    """
    Model for a new player
    """
    id: str = Field(..., description="ID of the player", example="123e4567-e89b-12d3-a456-426614174000")
    name: str = Field(..., description="Name of the player")
    email: str = Field(..., description="Email of the player")
    is_active: bool = Field(True, description="Is the player active?")
    is_banned: bool = Field(False, description="Is the player banned?")
    is_deleted: bool = Field(False, description="Is the player deleted?")
    is_verified: bool = Field(False, description="Is the player verified?")
    is_premium: bool = Field(False, description="Is the player premium?")
    level: int = Field(1, description="Level of the player")
    bankroll: float = Field((100*1000)*100, description="Bankroll of the player")

class Player(BaseModel):
    """
    Model for a player
    """
    id: str | uuid.UUID = Field(..., description="ID of the player", example="123e4567-e89b-12d3-a456-426614174000",  default_factory=postgres_uuid2str)
    name: str = Field(..., description="Name of the player")
    email: str = Field(..., description="Email of the player")
    is_active: bool = Field(True, description="Is the player active?")
    is_banned: bool = Field(False, description="Is the player banned?")
    is_deleted: bool = Field(False, description="Is the player deleted?")
    is_verified: bool = Field(False, description="Is the player verified?")
    is_premium: bool = Field(False, description="Is the player premium?")
    level: int = Field(1, description="Level of the player")
    bankroll: float = Field((100*1000)*100, description="Bankroll of the player")
    
    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if isinstance(self.id, uuid.UUID):
            self.id = str(self.id)