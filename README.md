# Authentication & Authorization Service with FastAPI and AWS Cognito

## Overview
This project is a Python-based Authentication and Authorization service built with FastAPI and AWS Cognito. It provides:

1. **Sign-in Functionality**: Authenticate users with AWS Cognito using username and password.
2. **Token Verification**: Validate JWT tokens via AWS Cognito to ensure their authenticity.
3. **Role-Based Access Control (RBAC)**: Restrict access to endpoints based on user roles defined in Cognito.

The project uses `pdm` for dependency management and is designed to run on Python 3.11.

## Features
- **User Authentication**: Users can log in using their Cognito credentials.
- **Token Validation**: Securely validate tokens by interacting with AWS Cognito.
- **RBAC Decorator**: Enforce access control for endpoints based on user roles stored in Cognito.
- **AWS Cognito Integration**: Seamless integration with Cognito for user management and authentication flows.

## Requirements
- Python 3.11
- AWS account with permissions to manage Cognito resources.
- AWS Cognito User Pool and App Client configured with the `USER_PASSWORD_AUTH` flow enabled.

## Setup

### 1. Clone the Repository
```bash
git clone <repository_url>
cd <repository_directory>
```

### 2. Install `pdm`
If you don’t have `pdm` installed:
```bash
pip install pdm
```

### 3. Install Dependencies
Run the following command to install the project dependencies:
```bash
pdm install
```

### 4. Configure Environment Variables
Set the following environment variables:

- `AWS_REGION`: The AWS region where your Cognito User Pool is hosted (e.g., `us-east-1`).
- `COGNITO_USER_POOL_ID`: Your Cognito User Pool ID (e.g., `us-east-1_XXXXXXXXX`).
- `COGNITO_CLIENT_ID`: Your Cognito App Client ID.
- `COGNITO_CLIENT_SECRET`: Your Cognito App Client Secret (only if the App Client uses a secret).

Example:
```bash
export AWS_REGION=us-east-1
export COGNITO_USER_POOL_ID=us-east-1_XXXXXXXXX
export COGNITO_CLIENT_ID=XXXXXXXXXXXXXXXXXXXXXXXXXX
export COGNITO_CLIENT_SECRET=YYYYYYYYYYYYYYYYYYYYYYYYYYYY
```

### 5. Run the Application
Start the FastAPI application:
```bash
pdm run python main.py
```
The service will start at `http://localhost:8000`.

## Usage

### Sign-In Endpoint
- **URL**: `POST /signin`
- **Description**: Authenticates a user with Cognito using their username and password.
- **Request Body**:
```json
{
  "username": "testuser",
  "password": "testpassword"
}
```
- **Response**:
```json
{
  "access_token": "<JWT Access Token>",
  "id_token": "<JWT ID Token>",
  "refresh_token": "<Refresh Token>",
  "token_type": "Bearer"
}
```

### Token Verification Endpoint
- **URL**: `GET /verify_token`
- **Description**: Validates a token and retrieves user information.
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Response**:
```json
{
  "username": "testuser",
  "roles": ["support", "admin"]
}
```

### Protected Endpoint (Role-Based Access)
- **URL**: `GET /protected_support`
- **Description**: Access restricted to users with the `support` role.
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Response**:
```json
{
  "message": "Hello testuser, you have access to support resources!"
}
```

### Another Protected Endpoint
- **URL**: `GET /protected_admin`
- **Description**: Access restricted to users with the `admin` role.
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Response**:
```json
{
  "message": "Hello testuser, you have admin privileges!"
}
```

## Project Structure
```
aws-cognito/
├── src/
    ├──auth/
    │   ├── __init__.py          # Package initializer
    │   ├── cognito.py           # AWS Cognito integration
    │   ├── dependencies.py      # Role-based access control & user validation
    │   ├── models.py            # Pydantic models for requests and responses
    │   └── utils.py             # Helper functions
├── main.py                  # FastAPI application
├── pyproject.toml           # Project metadata and dependencies
├── README.md                # Project documentation
└── tests/                   # (Optional) Directory for test cases
```

## Configuration
### AWS Cognito Setup
1. Create a **Cognito User Pool**.
2. Create an **App Client** with the `USER_PASSWORD_AUTH` flow enabled.
3. Note the **User Pool ID**, **App Client ID**, and optionally **App Client Secret**.

### Environment Variables
Ensure the following variables are configured:
- `AWS_REGION`
- `COGNITO_USER_POOL_ID`
- `COGNITO_CLIENT_ID`
- `COGNITO_CLIENT_SECRET` (if using secret-based authentication).

## Notes
- Ensure that your Cognito App Client has the correct flows enabled (`USER_PASSWORD_AUTH`).
- Role-based access control assumes roles are stored as a comma-separated list in a custom attribute (`custom:role`). Update this as needed in `auth/cognito.py`.

## Contributing
Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

