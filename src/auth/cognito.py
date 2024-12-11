import boto3
from fastapi import HTTPException, status

from src.auth.models import CognitoUser
from src.auth.utils import (AWS_REGION, COGNITO_CLIENT_ID,
                            COGNITO_CLIENT_SECRET, USER_ROLE_ATTRIBUTE,
                            calculate_secret_hash)

cognito_client = boto3.client("cognito-idp", region_name=AWS_REGION)


def initiate_auth(username: str, password: str) -> dict:
    """
    Initiate AUTH flow with Cognito using USER_PASSWORD_AUTH.
    """
    auth_params = {
        "USERNAME": username,
        "PASSWORD": password
    }

    # If a client secret is required, add SECRET_HASH
    if COGNITO_CLIENT_SECRET:
        auth_params["SECRET_HASH"] = calculate_secret_hash(
            username, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET)

    try:
        response = cognito_client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters=auth_params,
            ClientId=COGNITO_CLIENT_ID
        )
        return response["AuthenticationResult"]
    except cognito_client.exceptions.NotAuthorizedException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    except cognito_client.exceptions.UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during authentication: {str(e)}"
        )


def get_user_from_token(access_token: str) -> CognitoUser:
    """
    Verify the token by calling GetUser in Cognito and retrieve user attributes including roles.
    """
    try:
        user_response = cognito_client.get_user(AccessToken=access_token)
        username = user_response.get("Username", "")
        attributes = user_response.get("UserAttributes", [])
        user_roles = []

        for attr in attributes:
            if attr["Name"] == USER_ROLE_ATTRIBUTE:
                # Assume roles are stored as a comma-separated string
                user_roles = [r.strip()
                              for r in attr["Value"].split(",") if r.strip()]
                break

        return CognitoUser(username=username, roles=user_roles)
    except cognito_client.exceptions.NotAuthorizedException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token."
        )
    except cognito_client.exceptions.UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or invalid token."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token verification failed: {str(e)}"
        )
