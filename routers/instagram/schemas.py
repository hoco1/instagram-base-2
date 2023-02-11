from pydantic import BaseModel,Field

class Account(BaseModel):
    instagramID:str = Field(default=None)
    instagramPass:str = Field(default=None)

class Cookie(BaseModel):
    _id:str
    csrftoken:str
    rur:str
    mid:str
    ds_user_id:str
    ig_did:str
    sessionid:str