import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import date, timedelta

client = TestClient(app)

def test_article_search_basic():
    """Test basic article search with just a query term"""
    response = client.get("/nytimes/articlesearch?q=python")
    assert response.status_code == 200
    data = response.json()
    
    assert "results" in data
    
    # Only check field structure if we got results
    if data["results"]:
        for article in data["results"]:
            assert "headline" in article
            assert "snippet" in article
            assert "web_url" in article
            assert "pub_date" in article

def test_article_search_with_dates():
    """Test article search with date parameters"""
    today = date.today()
    last_year = today.replace(year=today.year - 1)
    begin_date = last_year - timedelta(days=30)
    end_date = last_year
    
    response = client.get(f"/nytimes/articlesearch?q=python&begin_date={begin_date}&end_date={end_date}")
    assert response.status_code == 200

def test_article_search_with_sort():
    """Test article search with sort parameter"""
    response = client.get("/nytimes/articlesearch?q=python&sort=newest")
    assert response.status_code == 200

def test_article_search_with_filter_query():
    response = client.get("/nytimes/articlesearch?q=python&filter_query=section_name:(\"Technology\")")
    assert response.status_code == 200

def test_empty_query():
    response = client.get("/nytimes/articlesearch?q=")
    assert response.status_code == 422

def test_invalid_sort():
    """Test that invalid sort parameter returns 400 error"""
    response = client.get("/nytimes/articlesearch?q=python&sort=invalid")
    assert response.status_code == 400
    assert "Sort parameter must be one of" in response.json()["detail"]

def test_future_date():
    future_date = date.today() + timedelta(days=30)
    response = client.get(f"/nytimes/articlesearch?q=python&begin_date={future_date}")
    assert response.status_code == 400
    assert "cannot be in the future" in response.json()["detail"]

def test_end_before_begin():
    today = date.today()
    yesterday = today - timedelta(days=1)
    response = client.get(f"/nytimes/articlesearch?q=python&begin_date={today}&end_date={yesterday}")
    assert response.status_code == 400
    assert "cannot be before begin date" in response.json()["detail"]

def test_no_results():
    response = client.get("/nytimes/articlesearch?q=xyzabc123notfoundterm")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 0