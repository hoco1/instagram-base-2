from .schemas import TokenData
from core.config import settings
from db import get_database

from jose import jwt
from jose import JWTError

from fastapi.security import OAuth2PasswordBearer
from fastapi import status
from fastapi import HTTPException,Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme),db=Depends(get_database)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await db.get_account(token_data.username)
    if user is None:
        raise credentials_exception
    return user