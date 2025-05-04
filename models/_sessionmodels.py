from pydantic import BaseModel, Field, validate_call
from typing_extensions import Optional, Dict, Any, Annotated
from datetime import datetime

class Session(BaseModel):
    """
    Model for a session
    """
    iss: str = Field(..., description="ID of the session", example="123e4567-e89b-12d3-a456-426614174000")
    sub: str = Field(..., description="ID of the player", example="123e4567-e89b-12d3-a456-426614174000")
    session_id: str = Field(..., description="ID of the session", example="123e4567-e89b-12d3-a456-426614174000")
    refresh_token: str = Field(..., description="Refresh token of the session")
    exp: int = Field(..., description="Expiration time of the session", example=1672531199)
    #convert exp to datetime
    exp_dt: Optional[datetime] = Field(None, description="Expiration time of the session in datetime format", example="2023-01-01T00:00:00Z")
    iat: int = Field(..., description="Issued at time of the session", example=1672531199)
    #convert iat to datetime
    iat_dt: Optional[datetime] = Field(None, description="Issued at time of the session in datetime format", example="2023-01-01T00:00:00Z")
    
    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if self.exp:
            self.exp_dt = datetime.fromtimestamp(self.exp)
        if self.iat:
            self.iat_dt = datetime.fromtimestamp(self.iat)


#