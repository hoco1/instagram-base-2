from pydantic import BaseModel,Field
from typing import Optional,Union,Dict
class Account(BaseModel):
    instagramID:Optional[Union[None,str] ]
    instagramPass:Union[None,str] 
    cookie:Optional[Dict]

class Cookie(BaseModel):
    _id:str
    csrftoken:str
    rur:str
    mid:str
    ds_user_id:str
    ig_did:str
    sessionid:str