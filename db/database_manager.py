from core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import List
from core.hashing import Hasher
class MongoManager:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(self, path: str):
        self.client = AsyncIOMotorClient(
            path,
            maxPoolSize=10,
            minPoolSize=10)
        self.db = self.client[settings.DATABASE]
        
    async def close_database_connection(self):
        self.client.close()
        
    async def add_account(self,user):
        user['password'] = Hasher.get_password_hash(user['password'])
        await self.db[settings.TABLE_USERS].insert_one(user)
    
    async def get_account(self,username):
        user = await self.db[settings.TABLE_USERS].find_one({"username":username})
        return user
    
    async def get_cookie(self,userPanel):
        cursor = self.db[settings.TABLE_INSTAGRAM_COOKIE].find({'userPanel':userPanel}).sort("_id",-1).limit(1)
        cookie = []
        async for i in cursor:
            cookie.append(i)
        print(cookie)
        cookie = cookie[0]
        del cookie['_id']
        del cookie['username']
        del cookie['userPanel']
        return cookie
    
    async def add_instagram_account(self,data):
        await self.db[settings.TABLE_INSTAGRAM_ACCOUNTS].insert_one(data)
    
    async def get_instagram_accounts(self,userPanel):
        list_accounts = []
        accounts = self.db[settings.TABLE_INSTAGRAM_ACCOUNTS].find({'userPanel':userPanel})
        async for account in accounts:
            list_accounts.append(account)
        return list_accounts

    async def add_cookie(self,cookie):
        await self.db[settings.TABLE_INSTAGRAM_COOKIE].insert_one(dict(cookie))
        
    
    async def add_follower(self,user):
        await self.db[settings.TABLE_INSTAGRAM_FOLLOWERS].insert_one(user)
        
    async def fetch_follower_data(self,username,limitation=15):
        list_followers = []
        followers =  self.db[settings.TABLE_INSTAGRAM_FOLLOWERS].find({'which_account':username}).limit(limitation)
        async for follower in followers:
            list_followers.append(follower)
        return list_followers
    
    async def add_following(self,user):
        await self.db[settings.TABLE_INSTAGRAM_FOLLOWING].insert_one(user)
        
    async def fetch_following_data(self,username,limitation=15):
        list_following = []
        following =  self.db[settings.TABLE_INSTAGRAM_FOLLOWING].find({'which_account':username}).limit(limitation)
        async for i in following:
            list_following.append(i)
        return list_following
        
    