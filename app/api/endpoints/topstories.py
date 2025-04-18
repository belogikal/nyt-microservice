from fastapi import APIRouter, HTTPException, Path
from app.models.topstories import TopStoriesResponse, TopStoryArticle
from app.services.nyt_api import fetch_top_stories
from typing import List
import time
import asyncio

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
    
    # Start timing total fetching process
    total_fetch_start = time.time()
    
    # Create tasks for concurrent execution
    fetch_tasks = {section: fetch_top_stories(section) for section in sections}
    
    # Execute all API calls concurrently
    try:
        # Wait for all tasks to complete
        fetch_results = await asyncio.gather(*fetch_tasks.values(), return_exceptions=True)
        section_fetch_times = {}
        
        # Process results
        for section, data in zip(sections, fetch_results):
            section_end = time.time()
            section_fetch_times[section] = section_end - total_fetch_start
            
            if isinstance(data, Exception):
                raise HTTPException(status_code=500, 
                                   detail=f"Error fetching {section} stories: {str(data)}")
            
            articles = data.get("results", [])
            
            # Take the two most recent articles
            section_articles = []
            for article in articles[:2]:
                section_articles.append(
                    TopStoryArticle(
                        title=article.get("title", ""),
                        section=article.get("section", ""),
                        url=article.get("url", ""),
                        abstract=article.get("abstract", ""),
                        published_date=article.get("published_date", "")
                    )
                )
            
            result[section] = section_articles
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stories: {str(e)}")
    
    # End timing total fetch process
    total_fetch_end = time.time()
    
    # Time the response preparation
    response_prep_start = time.time()
    response = TopStoriesResponse(**result)
    response_prep_end = time.time()
    
    # Print timing information
    print("\n--- Timing Information ---")
    print(f"Raw API fetch times:")
    for section, fetch_time in section_fetch_times.items():
        print(f"  - {section}: {fetch_time:.4f} seconds")
    print(f"Total time for all API fetches: {total_fetch_end - total_fetch_start:.4f} seconds")
    print(f"Response preparation time: {response_prep_end - response_prep_start:.4f} seconds")
    print(f"Total endpoint execution time: {response_prep_end - total_fetch_start:.4f} seconds")
    print("-------------------------\n")
    
    return response