from fastapi import APIRouter, HTTPException
from app.models.topstories import TopStoriesResponse, TopStoryArticle
from app.services.nyt_api import fetch_top_stories
import asyncio
from datetime import datetime

router = APIRouter()

@router.get("/topstories", response_model=TopStoriesResponse, summary="Get Top Stories")
async def get_top_stories():
    """
    Retrieve the two most recent top stories from each of the following categories:
    - arts
    - food
    - movies
    - travel
    - science
    
    Returns a compiled list of articles from each section.
    """
    sections = ["arts", "food", "movies", "travel", "science"]
    result = {}
    
    fetch_tasks = {section: fetch_top_stories(section) for section in sections}
    
    try:
        fetch_results = await asyncio.gather(*fetch_tasks.values(), return_exceptions=True)
        
        for section, data in zip(sections, fetch_results):
            if isinstance(data, Exception):
                raise HTTPException(status_code=500, 
                                   detail=f"Error fetching {section} stories: {str(data)}")
            
            articles = data.get("results", [])
            
            # Filter out invalid articles
            valid_articles = []
            for article in articles:
                # Check that required fields have data
                if (article.get("title") and 
                    article.get("url") and 
                    article.get("abstract") and 
                    article.get("published_date")):
                    valid_articles.append(article)
            
            # Sort by published_date to get the most recent
            valid_articles.sort(
                key=lambda x: datetime.fromisoformat(x["published_date"].replace("Z", "+00:00")), 
                reverse=True
            )
            
            # Take the two most recent valid articles
            section_articles = []
            for article in valid_articles[:2]:
                section_articles.append(
                    TopStoryArticle(
                        title=article.get("title", ""),
                        section=article.get("section", ""),
                        url=article.get("url", ""),
                        abstract=article.get("abstract", ""),
                        published_date=article.get("published_date", "")
                    )
                )
            
            # Handle the case where a section doesn't have enough valid articles
            if len(section_articles) < 2:
                # Add placeholder articles if needed for the response model
                while len(section_articles) < 2:
                    section_articles.append(
                        TopStoryArticle(
                            title=f"No recent {section} story available",
                            section=section,
                            url="",
                            abstract="No recent content available for this section.",
                            published_date=datetime.now().isoformat()
                        )
                    )
            
            result[section] = section_articles
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stories: {str(e)}")
    
    response = TopStoriesResponse(**result)
    return response