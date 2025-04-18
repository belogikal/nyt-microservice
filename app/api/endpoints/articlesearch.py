from fastapi import APIRouter, HTTPException, Query
from datetime import date
from typing import Optional, List
from app.models.articlesearch import ArticleSearchResponse, ArticleSearchResult  
from app.services.nyt_api import search_articles

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

        data = await search_articles(q, begin_date, end_date)
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
        
        return ArticleSearchResponse(results=articles)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching articles: {str(e)}")