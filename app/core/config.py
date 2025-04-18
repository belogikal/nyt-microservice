import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "NYTimes Article Microservice"
    NYT_API_KEY: str = os.getenv("NYT_API_KEY")
    NYT_TOP_STORIES_BASE_URL: str = "https://api.nytimes.com/svc/topstories/v2"
    NYT_ARTICLE_SEARCH_URL: str = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

    class Config:
        case_sensitive = True

settings = Settings()