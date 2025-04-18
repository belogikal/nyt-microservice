import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

def test_get_top_stories():
    """Test successful retrieval of top stories with default sections"""
    response = client.get("/nytimes/topstories")
    assert response.status_code == 200
    data = response.json()
    
    # Check that all required sections are present
    required_sections = ["arts", "food", "movies", "travel", "science"]
    for section in required_sections:
        assert section in data
        
        # Check that each section has exactly 2 articles
        assert len(data[section]) == 2
        
        # Check that each article has the required fields
        for article in data[section]:
            assert "title" in article
            assert "section" in article
            assert "url" in article
            assert "abstract" in article
            assert "published_date" in article

@pytest.mark.parametrize("mock_key", ["empty_results", "missing_fields", "invalid_date"])
def test_error_handling(mock_key, monkeypatch):
    """Test handling of various error scenarios"""
    
    async def mock_fetch_empty_results(section):
        return {"results": []}
    
    async def mock_fetch_missing_fields(section):
        return {"results": [
            {"title": "Test Article", "section": "arts"},  # Missing url, abstract, etc.
            {}  # Completely empty article
        ]}
    
    async def mock_fetch_invalid_date(section):
        return {"results": [
            {
                "title": "Test Article",
                "section": "arts",
                "url": "https://example.com",
                "abstract": "Test abstract",
                "published_date": "invalid-date"
            }
        ]}
    
    if mock_key == "empty_results":
        monkeypatch.setattr("app.services.nyt_api.fetch_top_stories", mock_fetch_empty_results)
    elif mock_key == "missing_fields":
        monkeypatch.setattr("app.services.nyt_api.fetch_top_stories", mock_fetch_missing_fields)
    elif mock_key == "invalid_date":
        monkeypatch.setattr("app.services.nyt_api.fetch_top_stories", mock_fetch_invalid_date)
    
    response = client.get("/nytimes/topstories")
    assert response.status_code == 200
    
    # Even with errors, we should have placeholder articles
    data = response.json()
    # Just check that we have the expected sections
    assert "arts" in data
    assert "food" in data
    assert "movies" in data
    assert "travel" in data
    assert "science" in data