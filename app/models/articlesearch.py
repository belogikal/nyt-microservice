from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class ArticleSearchQuery(BaseModel):
    q: str = Field(..., description="Search query term")
    begin_date: Optional[date] = Field(None, description="Start date for results (format: YYYYMMDD)")
    end_date: Optional[date] = Field(None, description="End date for results (format: YYYYMMDD)")

class ArticleSearchResult(BaseModel):
    headline: str = Field(..., description="The article headline")
    snippet: str = Field(..., description="A brief snippet from the article")
    web_url: str = Field(..., description="The URL of the article")
    pub_date: str = Field(..., description="The date when the article was published")

class ArticleSearchResponse(BaseModel):
    results: List[ArticleSearchResult] = Field(..., description="List of articles matching the search criteria")