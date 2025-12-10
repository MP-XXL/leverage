from fastapi import FastAPI
from models.base import Base
from database.database_main import engine
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title = "Leverage",
    version = "0.0.1 Beta"
)

@app.get("/")
def home():
    return {
        "message":"Welcome to a world of financial freedom. We provide, Leverage!"
    }