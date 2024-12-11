import base64
import hashlib
import hmac
import os

from dotenv import load_dotenv

load_dotenv(override=True)

# Utility functions and constants
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
COGNITO_USER_POOL_ID = os.environ.get(
    "COGNITO_USER_POOL_ID", "<your_user_pool_id>")
COGNITO_CLIENT_ID = os.environ.get("COGNITO_CLIENT_ID", "<your_client_id>")
COGNITO_CLIENT_SECRET = os.environ.get(
    "COGNITO_CLIENT_SECRET", None)  # If required
# Adjust if your roles are stored differently
USER_ROLE_ATTRIBUTE = "custom:role"


def calculate_secret_hash(username: str, client_id: str, client_secret: str) -> str:
    """
    Calculate the Cognito SECRET_HASH using HMAC SHA256 for secret-enabled clients.
    """
    msg = username + client_id
    dig = hmac.new(client_secret.encode('utf-8'),
                   msg.encode('utf-8'), hashlib.sha256).digest()
    return base64.b64encode(dig).decode()
