from fastapi import FastAPI
from .models.base import Base
from .database.database_main import engine
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def db_and_table_init():
    retries = 10
    for i in range(retries):
        try:
            logger.info("STARTING APPLICATION!")
            Base.metadata.create_all(bind=engine)
            logger.info("DATABASE INITIALIZED SUCCESSFULLY!")
            break
        except OperationalError as e:
            logger.warning(f"MySQL NOT READY, RETRYING ({i+1}/{retries}) {e}...")
            time.sleep(3)
        except Exception as e:
            logger.info(f"DATABASE INITIALIZATION FAILED: {e}")


app = FastAPI(
    title = "Leverage",
    version = "0.0.1 Beta"
)

@app.on_event("startup")
def on_startup():
    db_and_table_init()


@app.get("/")
def home():
    return {
        "message":"Welcome to a world of financial freedom. We provide, Leverage!"
    }