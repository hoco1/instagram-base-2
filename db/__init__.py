from .database_manager import MongoManager

database = MongoManager()

async def get_database():
    return database