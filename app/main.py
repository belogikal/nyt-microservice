from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A microservice to access NYTimes articles data",
    version="0.1.0",
)

@app.get("/")
async def root():
    return {"message": "Welcome to NYTimes Article Microservice"}