from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.database import init_db
from app.routes import users,posts,comments
from fastapi.exceptions import RequestValidationError
from app.exception_handlers import http_exception_handler, request_validation_exception_handler

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

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)