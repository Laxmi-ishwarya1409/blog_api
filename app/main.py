from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.routes import users,posts,comments
from app.routes import users,posts,comments

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Server is starting")
    await init_db()
    yield
    print("Server has been stopped")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "Blog API is running"}

app.include_router(users.router, prefix = "/users",tags = ["Users"])
app.include_router(posts.router, prefix = "/posts",tags = ["Posts"])
app.include_router(comments.router, prefix = "/comments",tags = ["Comments"])