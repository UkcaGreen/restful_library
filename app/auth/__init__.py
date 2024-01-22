import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from config import settings

basic_auth = HTTPBasic(auto_error=False)


def authent(
    credentials: HTTPBasicCredentials = Depends(basic_auth),
):
    if check_basic_auth_creds(credentials):
        return True

    raise HTTPException(status_code=403, detail="invalid username or password provided")


def check_basic_auth_creds(
    credentials: HTTPBasicCredentials = Depends(basic_auth),
):
    if not credentials:
        return False

    correct_username = secrets.compare_digest(
        credentials.username, settings.API_USERNAME
    )
    correct_password = secrets.compare_digest(
        credentials.password, settings.API_PASSWORD
    )

    if correct_username and correct_password:
        return True

    return False
