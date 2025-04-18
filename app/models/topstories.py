from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TopStoryArticle(BaseModel):
    title: str = Field(..., description="The article title")
    section: str = Field(..., description="The section the article belongs to")
    url: str = Field(..., description="The URL of the article")
    abstract: str = Field(..., description="A brief summary of the article")
    published_date: str = Field(..., description="The date when the article was published")

class TopStoriesResponse(BaseModel):
    arts: List[TopStoryArticle] = Field(..., description="Top articles from the arts section")
    food: List[TopStoryArticle] = Field(..., description="Top articles from the food section")
    movies: List[TopStoryArticle] = Field(..., description="Top articles from the movies section")
    travel: List[TopStoryArticle] = Field(..., description="Top articles from the travel section")
    science: List[TopStoryArticle] = Field(..., description="Top articles from the science section")