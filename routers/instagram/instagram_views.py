from core.auth.jwt_bearer import get_current_user
from .schemas import Account,Cookie
from db import get_database,database
from core.config import settings

from core.scarping import InstagramScrapping

from .showing_data import serializeList

from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()
scrap = InstagramScrapping()

# save (user,pass) and cookie
@router.post('/instagram',tags=['instagram'])
async def add_user(instagram:Account,dependencies = Depends(get_current_user),db=Depends(get_database)) -> Cookie:
    username = instagram.instagramID
    password = instagram.instagramPass
    
    await scrap.account(username, password)
    cookie = await database.get_cookie()
    return cookie

# get following list
@router.get("/instagram/following/{usr}",tags=['instagram'])
async def list_following(username:str,dependencies = Depends(get_current_user),db=Depends(get_database)):
    await scrap.following(username)
    res = await db.fetch_following_data(username,10)
    return serializeList(res)
    
# get follower list
@router.get("/instagram/follower/{usr}",tags=['instagram'])
async def list_follower(username:str,dependencies = Depends(get_current_user),db=Depends(get_database)):
    await scrap.follower(username)
    res = await db.fetch_follower_data(username,10)
    return serializeList(res)

