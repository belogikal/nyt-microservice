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
                # Handle API exceptions - create placeholder articles
                result[section] = create_placeholder_articles(section, 2)
                continue
                
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
            
            try:
                valid_articles.sort(
                    key=lambda x: datetime.fromisoformat(x["published_date"].replace("Z", "+00:00")), 
                    reverse=True
                )
            except (ValueError, TypeError):
                # If date parsing fails, don't crash
                pass
            
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
            
            if len(section_articles) < 2:
                placeholders = create_placeholder_articles(section, 2 - len(section_articles))
                section_articles.extend(placeholders)
            
            result[section] = section_articles
            
    except Exception as e:
        # If something catastrophic happens, still provide a valid response
        for section in sections:
            if section not in result:
                result[section] = create_placeholder_articles(section, 2)
    
    response = TopStoriesResponse(**result)
    return response

def create_placeholder_articles(section, count):
    """Helper function to create placeholder articles"""
    articles = []
    for _ in range(count):
        articles.append(
            TopStoryArticle(
                title=f"No recent {section} story available",
                section=section,
                url="",
                abstract="No recent content available for this section.",
                published_date=datetime.now().isoformat()
            )
        )
    return articles