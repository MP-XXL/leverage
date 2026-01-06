from fastapi import FastAPI
from models.base import Base
from database.database_main import engine
from routes import users_routes, auth_route, verification_route, accounts_routes, admin_routes
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title = "Leverage",
    version = "0.0.1 Beta"
)

app.include_router(users_routes.router)
app.include_router(auth_route.router)
app.include_router(verification_route.router)
app.include_router(accounts_routes.router)
app.include_router(admin_routes.router)

@app.get("/")
def home():
    return {
        "message":"Welcome to a world of financial freedom. We provide, Leverage!"
    }