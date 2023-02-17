from pydantic import BaseModel,Field
from typing import Optional,Union,Dict
class Account(BaseModel):
    instagramID:Optional[str]
    instagramPass:Optional[str] 
    cookie:Optional[Union[dict,list,None]]
class UserPanel(BaseModel):
    username:str
class Instagram(BaseModel):
    message:str
    cookie:Optional[str]
class FetchData(BaseModel):
    instagramID:str
    whichAccount:str

class ResponseLogin(BaseModel):
    first_name:Optional[str]
    last_name:Optional[str]
    email:Optional[str]
    is_email_confirmed:Optional[str]
    is_phone_confirmed:Optional[str]
    username:Optional[str]
    phone_number:Optional[str]
    gender:Optional[str]
    birthday:Optional[str]
    cookie:Optional[dict]