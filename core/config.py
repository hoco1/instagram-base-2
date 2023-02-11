from decouple import config

class Settings:
    # Authentication users
    SECRET_KEY: str = config("SECRET_KEY")
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30 # in mins
    # MongoDB 
    MONGO_HOST:str=config("MONGO_HOST")
    MONGO_USER=config("MONGO_USER")
    MONGO_PASSWORD=config("MONGO_PASSWORD")
    # Database and Table names
    DATABASE="local"
    TABLE_USERS="users"
    TABLE_INSTAGRAM_ACCOUNTS="accounts"
    TABLE_INSTAGRAM_COOKIE="cookies"
    TABLE_INSTAGRAM_FOLLOWERS="followers"
    TABLE_INSTAGRAM_FOLLOWING="following"

settings=Settings()
    