from .schemas import Token,UserIn,UserOut
from core.config import settings
from db import database,get_database
from core.hashing import Hasher
from core.auth.jwt_handler import create_access_token

from datetime import timedelta
from typing import Any,List

from fastapi import APIRouter
from fastapi import responses,status,Body
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException,Depends

router = APIRouter()

@router.post('/register',tags=['users'],response_model=UserOut)
async def create_user(user:UserIn,db=Depends(get_database)):
    user = dict(user)
    await db.add_account(user)
    return user
    
@router.post("/token", response_model=Token,tags=['users'],)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db=Depends(get_database)):
    
    user = await db.get_account(form_data.username)
    if  not user or not Hasher.verify_password(form_data.password,user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub":user['username']},expires_delta=access_token_expires
    )

    return {"access_token":access_token, "token_type": "bearer"}



