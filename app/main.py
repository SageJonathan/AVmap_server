from fastapi import FastAPI

from app.routes import data_router

app = FastAPI(title="AVmap Server")

app.include_router(data_router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}