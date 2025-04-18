import httpx
from app.core.config import settings
from typing import Dict, Any, List
from datetime import date

async def fetch_top_stories(section: str) -> Dict[str, Any]:
    """Fetch top stories from NYT API for a specific section"""
    url = f"{settings.NYT_TOP_STORIES_BASE_URL}/{section}.json"
    params = {"api-key": settings.NYT_API_KEY}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()

async def search_articles(query: str, begin_date: date = None, end_date: date = None) -> Dict[str, Any]:
    """Search for articles using the NYT Article Search API"""
    params = {
        "q": query,
        "api-key": settings.NYT_API_KEY,
    }
    
    if begin_date:
        params["begin_date"] = begin_date.strftime("%Y%m%d")
    
    if end_date:
        params["end_date"] = end_date.strftime("%Y%m%d")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(settings.NYT_ARTICLE_SEARCH_URL, params=params)
        response.raise_for_status()
        return response.json()