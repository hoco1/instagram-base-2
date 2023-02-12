from core.auth.jwt_bearer import get_current_user
from .schemas import Account,Cookie
from db import get_database,database
from core.config import settings

from core.scarping import InstagramScrapping

from .showing_data import serializeList

from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()

# save (user,pass) and cookie
@router.post('/instagram/login',tags=['instagram'])
async def add_user(instagram:Account,user = Depends(get_current_user),db=Depends(get_database)):
    username = instagram.instagramID
    password = instagram.instagramPass
    cookie = instagram.cookie
    scrap = InstagramScrapping(db)
    if len(cookie) > 0:
        res = await scrap.check_cookie(**cookie)
        if not res:
            return {"msg":"cookie is invalid"}
        await db.add_cookie(cookie)
        # cookies = await database.get_cookie()
        # return cookies
    else:
        res = await scrap.account(username, password)
        if not res:
            return {"msg":"username and password is invalid"}
        cookies = await database.get_cookie(instaID=username)
        return cookies

# get following list
@router.get("/instagram/following/{usr}",tags=['instagram'])
async def list_following(username:str,instaID:str ,user= Depends(get_current_user),db=Depends(get_database)):
    scrap = InstagramScrapping(db)
    await scrap.following(username,instaID)
    res = await db.fetch_following_data(username,10)
    return serializeList(res)
    
# get follower list
@router.get("/instagram/follower/{usr}",tags=['instagram'])
async def list_follower(username:str,instaID:str,user = Depends(get_current_user),db=Depends(get_database)):
    scrap = InstagramScrapping(db)
    await scrap.follower(username,instaID)
    res = await db.fetch_follower_data(username,10)
    return serializeList(res)

