from fastapi import FastAPI
from db import database
from core.config import settings
from routers.account import account_views
from routers.instagram import instagram_views


app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect_to_database(path=settings.MONGO_HOST)
    
@app.get('/',tags=['main'])
async def root(): 
    # cookie= await database.get_cookie()
    return {'Message':'Hi'}

app.include_router(account_views.router)
app.include_router(instagram_views.router)

@app.on_event("shutdown")
async def shutdown():
    await database.close_database_connection()