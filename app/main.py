from fastapi import FastAPI
from app.core.config import settings
from app.api.endpoints import topstories, articlesearch

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A microservice to access NYTimes articles data",
    version="0.1.0",
)

app.include_router(topstories.router, prefix="/nytimes", tags=["nytimes"])
app.include_router(articlesearch.router, prefix="/nytimes", tags=["nytimes"])

@app.get("/")
async def root():
    return {"message": "Welcome to NYTimes Article Microservice"}