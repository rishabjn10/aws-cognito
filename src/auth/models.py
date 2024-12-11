from typing import List, Optional

from pydantic import BaseModel, Field


class SigninRequest(BaseModel):
    """Request model for the signin endpoint."""
    username: str = Field(..., description="The user's username")
    password: str = Field(..., description="The user's password")


class TokenResponse(BaseModel):
    """Response model for successful authentication."""
    access_token: str = Field(..., description="Access JWT token from Cognito")
    id_token: str = Field(..., description="ID JWT token from Cognito")
    refresh_token: Optional[str] = Field(
        None, description="Refresh token from Cognito")
    token_type: str = Field(..., description="Type of the token returned")


class CognitoUser(BaseModel):
    """Model representing the user returned from token verification."""
    username: str
    roles: List[str]
