from functools import wraps
from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.auth.cognito import get_user_from_token
from src.auth.models import CognitoUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")


def get_current_user(token: str = Depends(oauth2_scheme)) -> CognitoUser:
    """
    Dependency to get the current user from the given token.
    This will verify the token with Cognito and return the user's information.
    """
    return get_user_from_token(token)


def require_roles(*required_roles: str) -> Callable:
    """
    Decorator for role-based access control.
    Use on endpoints to enforce that the user possesses all required roles.
    """

    def decorator(endpoint: Callable) -> Callable:
        @wraps(endpoint)
        def wrapper(*args, user: CognitoUser = Depends(get_current_user), **kwargs):
            user_roles = set(user.roles or [])
            needed_roles = set(required_roles)
            if not needed_roles.issubset(user_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have the required roles to access this endpoint.",
                )
            return endpoint(*args, user=user, **kwargs)

        return wrapper

    return decorator
