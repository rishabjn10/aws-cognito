import uvicorn
from fastapi import Depends, FastAPI

from src.auth.cognito import initiate_auth
from src.auth.dependencies import get_current_user, require_roles
from src.auth.models import CognitoUser, SigninRequest, TokenResponse

app = FastAPI(title="Auth & Authorization with FastAPI & Cognito")


@app.post("/signin", response_model=TokenResponse, summary="Signin Endpoint")
def signin(credentials: SigninRequest):
    """
    Sign-in endpoint to authenticate the user with AWS Cognito using username and password.
    On success, returns JWT tokens (access_token, id_token, refresh_token).
    """
    auth_result = initiate_auth(credentials.username, credentials.password)
    return TokenResponse(
        access_token=auth_result["AccessToken"],
        id_token=auth_result["IdToken"],
        refresh_token=auth_result.get("RefreshToken"),
        token_type="Bearer",
    )


@app.get("/verify_token", summary="Token Verification Example")
def verify_token(user: CognitoUser = Depends(get_current_user)):
    """
    Example endpoint to demonstrate token verification.
    If the token is valid, returns the user's username and roles.
    """
    return {"username": user.username, "roles": user.roles}


@app.get("/protected_support", summary="Protected endpoint for Support role")
@require_roles("support")
def protected_support_endpoint(user: CognitoUser = Depends(get_current_user)):
    """
    Protected endpoint that requires the 'support' role.
    If the user has 'support' role, returns success message.
    """
    return {"message": f"Hello {user.username}, you have access to support resources!"}


@app.get("/protected_admin", summary="Protected endpoint for Admin role")
@require_roles("admin")
def protected_admin_endpoint(user: CognitoUser = Depends(get_current_user)):
    """
    Protected endpoint that requires the 'admin' role.
    If the user has 'admin' role, returns success message.
    """
    return {"message": f"Hello {user.username}, you have admin privileges!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
