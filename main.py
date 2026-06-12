from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import Base, engine
import models

from routers.users import router as users_router
from routers.recipes import router as recipes_router
from routers.ratings import router as ratings_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(users_router)
app.include_router(recipes_router)
app.include_router(ratings_router)

@app.get("/")
def root():
    return {"message": "Recipe Management API"}