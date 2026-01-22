from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routers import users
from app.routers import users, notes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(notes.router)

@app.get("/")
def health():
    return {"status": "ok"}
