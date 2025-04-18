from fastapi import APIRouter, HTTPException, Query, Depends
from datetime import date
from typing import Optional, List
from app.models.articlesearch import ArticleSearchResponse, ArticleSearchResult  
from app.services.nyt_api import search_articles
import time

router = APIRouter()

@router.get("/articlesearch", response_model=ArticleSearchResponse, summary="Search Articles")
async def article_search(
    q: str = Query(..., description="Search query term"),
    begin_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)")
):
    """
    Search for New York Times articles based on query terms and optional date range.
    
    - **q**: Required search term
    - **begin_date**: Optional start date in YYYY-MM-DD format
    - **end_date**: Optional end date in YYYY-MM-DD format
    
    Returns articles matching the search criteria.
    """
    try:
        api_fetch_start = time.time()
        data = await search_articles(q, begin_date, end_date)
        api_fetch_end = time.time()
        
        response_prep_start = time.time()
        articles = []
        for doc in data.get("response", {}).get("docs", []):
            headline = doc.get("headline", {}).get("main", "")
            snippet = doc.get("snippet", "")
            web_url = doc.get("web_url", "")
            pub_date = doc.get("pub_date", "")
            
            articles.append(
                ArticleSearchResult(
                    headline=headline,
                    snippet=snippet,
                    web_url=web_url,
                    pub_date=pub_date
                )
            )
        
        response = ArticleSearchResponse(results=articles)
        response_prep_end = time.time()
        
        print("\n--- Timing Information ---")
        print(f"Raw API fetch time: {api_fetch_end - api_fetch_start:.4f} seconds")
        print(f"Response preparation time: {response_prep_end - response_prep_start:.4f} seconds")
        print(f"Total endpoint execution time: {response_prep_end - api_fetch_start:.4f} seconds")
        print("-------------------------\n")
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching articles: {str(e)}")