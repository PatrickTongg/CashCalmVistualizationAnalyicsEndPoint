import hashlib
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import service.Connector as Connector


# Hash password function
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# Security scheme
security = HTTPBasic()


def get_current_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username = credentials.username
    current_password_sha256 = hash_password(credentials.password)
    query = f"SELECT username WHERE username = {current_username} and password = {current_password_sha256}"
    connector = Connector.Connector()
    result = connector.execute(query)

    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
