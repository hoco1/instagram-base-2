from core.auth.jwt_bearer import get_current_user
from .schemas import Account,Instagram,User,FetchData
from db import get_database,database
from core.config import settings

from core.scarping import InstagramScrapping

from .manipulation import serializeList

from fastapi import APIRouter
from fastapi import Depends,HTTPException

router = APIRouter()

# save (user,pass) and cookie
@router.post('/instagram/login',tags=['instagram'])
async def add_user(instagram:Account,user:User = Depends(get_current_user),db=Depends(get_database)):
    username = instagram.instagramID
    password = instagram.instagramPass
    cookies = instagram.cookie
    scrap = InstagramScrapping(db,user['username'])
    if cookies:
        if type(cookies) == list:
            cookie = {}
            for i in range(len(cookies)):
                try:
                    key = cookies[i]['name']
                    value = cookies[i]['value']
                    cookie[key]=value
                except:
                    raise HTTPException(status_code=422, detail="list format is invalid")
            cookies = cookie
        res = await scrap.get_account_info(cookies)
        if not res:
            raise HTTPException(status_code=401, detail="cookie is invalid")
        
        cookies['userPanel']=user['username']
        insta = res['username']
        cookies['username']=insta
        await db.add_cookie(cookies)
        print("cookie is valid & insert")
        return cookies
    if username and password:
        res = await scrap.account(username,password)
        return serializeList(res)
    raise HTTPException(status_code=401, detail="invalid credentials")

# get following list
@router.post("/instagram/following/{usr}",tags=['instagram'])
async def list_following(data:FetchData ,user= Depends(get_current_user),db=Depends(get_database)):
    scrap = InstagramScrapping(db,userPanel=user['username'])
    instagramID = data.instagramID
    whichAccount = data.whichAccount
    print(whichAccount)
    print(instagramID)
    await scrap.following(instagramID)
    res = await db.fetch_following_data(instagramID,10)
    return serializeList(res)
    
# get follower list
@router.post("/instagram/follower/{usr}",tags=['instagram'])
async def list_follower(data:FetchData,user = Depends(get_current_user),db=Depends(get_database)):
    scrap = InstagramScrapping(db,userPanel=user['username'])
    instagramID = data.instagramID
    whichAccount = data.whichAccount
    print(whichAccount)
    print(instagramID)
    await scrap.follower(instagramID)
    res = await db.fetch_follower_data(instagramID,10)
    return serializeList(res)

