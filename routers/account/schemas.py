from pydantic import BaseModel,Field,EmailStr
from typing import Union

class Token(BaseModel):
    access_token: str
    token_type: str

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None
     