from core.auth.jwt_bearer import get_current_user
from .schemas import Account,UserPanel,FetchData,ResponseLogin
from db import get_database,database
from core.config import settings

from core.scarping import InstagramScrapping

from .manipulation import serializeList

from fastapi import APIRouter
from fastapi import Depends,HTTPException

from bson.objectid import ObjectId

router = APIRouter()

# save (user,pass) and cookie
@router.post('/instagram/login',tags=['instagram'],response_model=ResponseLogin)
async def add_user(instagram:Account,user:UserPanel = Depends(get_current_user),db=Depends(get_database)):
    username = instagram.instagramID
    password = instagram.instagramPass
    cookies = instagram.cookie
    obj = ObjectId()

    userPanel = userPanel = await db.get_account(user['username']) 

    scrap = InstagramScrapping(db,userPanel['username'])
    if cookies:
        if type(cookies) == list:
            manipulatCookie = {}
            for cookie in cookies:
                try:
                    key=cookie['name']
                    value=cookie['value']
                    manipulatCookie[key]=value
                except:
                    raise HTTPException(status_code=422, detail="list format is invalid")
            cookies = manipulatCookie
        res = await scrap.get_account_info(cookies)
        if not res:
            raise HTTPException(status_code=401, detail="cookie is invalid")

        usefulInfos = ['first_name','last_name','email','is_email_confirmed',
                            'is_phone_confirmed','username',
                            'phone_number','gender','birthday']
        data = {}
        for info in usefulInfos:
            if res[info]:
                    data[info]=res[info]
        
        result={
            "first_name":res['first_name'] ,
            "last_name":res['last_name'] ,
            "email":res['email'] ,
            "is_email_confirmed":res['is_email_confirmed'] ,
            "is_phone_confirmed":res['is_phone_confirmed'],
            "username":res['username'] ,
            "phone_number":res['phone_number'] ,
            "gender":res['gender'] ,
            "birthday":res['birthday'],
            "cookie":dict(cookies)
        }
        
        cookies['_id']=obj

        await db.add_cookie(cookies)
        
        usr = data['username']
        instagramAccount = await db.get_instagram_account(usr)
        if instagramAccount:
            print(instagramAccount)
            myquery = { "username": usr }
            newvalues = { "$set": { "cookie_id": obj } }

            await db.update_instagram_account(myquery,newvalues)
            
            return result

        data['password_instagram']=None
        data['userPanel_id']=userPanel['_id']
        data['cookie_id'] = obj

        await db.add_instagram_account(data)

        return result
    if username and password:
        print(username,password)
        cookie,data = await scrap.account(username,password)
        res={
            "first_name": data["first_name"],
            "last_name": data.get("last_name",None),
            "email": data["email"],
            "is_email_confirmed": data.get("is_email_confirmed",None),
            "is_phone_confirmed": data.get("is_phone_confirmed",None),
            "username": data["username"],
            "phone_number": data.get("phone_number",None),
            "gender": data["gender"],
            "birthday": data["birthday"],
            "cookie":dict(cookie)
        }
        return res
    raise HTTPException(status_code=401, detail="invalid credentials")

# get following list
@router.post("/instagram/following/{usr}",tags=['instagram'])
async def list_following(data:FetchData ,user= Depends(get_current_user),db=Depends(get_database)):
    scrap = InstagramScrapping(db,userPanel=user['username'])
    instagramID = data.instagramID
    whichAccount = data.whichAccount
    await scrap.following(instagramID,whichAccount)
    res = await db.fetch_following_data(instagramID,10)
    return serializeList(res)
    
# get follower list
@router.post("/instagram/follower/{usr}",tags=['instagram'])
async def list_follower(data:FetchData,user = Depends(get_current_user),db=Depends(get_database)):
    scrap = InstagramScrapping(db,userPanel=user['username'])
    instagramID = data.instagramID
    whichAccount = data.whichAccount
    await scrap.follower(instagramID,whichAccount)
    res = await db.fetch_follower_data(instagramID,10)
    return serializeList(res)

