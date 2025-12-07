from fastapi import FastAPI


app = FastAPI(
    title = "Leverage",
    version = "0.0.1 Beta"
)


@app.get("/")
def home():
    return {
        "message":"Welcome to a world of financial freedom. We provide, Leverage!"
    }