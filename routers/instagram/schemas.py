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
    whichAccount:Optional[str]

class ResponseLogin(BaseModel):
    gender:str
    username:str
    email:str
    cookie:dict

