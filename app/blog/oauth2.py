from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from blog import token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token.verify_token(data, credentials_exception)
