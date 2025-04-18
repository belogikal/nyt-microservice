# NYTimes Article Microservice

A lightweight microservice built with FastAPI that integrates with the New York Times API to provide access to top stories and article search functionality.

## Overview

This microservice serves as a wrapper around two NYT API endpoints:

- Top Stories API - Fetches the latest articles from different sections
- Article Search API - Enables searching articles by keywords and date ranges

The service is deployed at [https://nyt-microservice.onrender.com/docs](https://nyt-microservice.onrender.com/docs)

## Features

- RESTful API design with clear request/response models
- Comprehensive error handling
- Input validation
- Asynchronous API calls for improved performance
- Automatic OpenAPI documentation

## Endpoints

### `/nytimes/topstories`

Returns the two most recent articles from five key NYT sections: arts, food, movies, travel, and science.

**Approach:**

- Concurrent API calls to improve response time
- Data filtering to ensure complete article information
- Chronological sorting to get the most recent articles
- Fallback mechanism with placeholder data for any issues

Each article includes what was required in the assessment:

- title
- section
- url
- abstract
- published_date

### `/nytimes/articlesearch`

Searches articles based on keywords and optional date ranges.

**Approach:**

- Flexible query parameters for customized searches
- Support for date range filtering
- Advanced filtering with the filter_query parameter
- Sorting options (relevance, newest, oldest)
- Clean response structure

Each search result includes again includes what was required in the assessment:

- headline
- snippet
- web_url
- pub_date

## Technical Stack

- Python 3.9+
- FastAPI framework
- Pydantic for data validation
- httpx for asynchronous HTTP requests
- pytest for testing
- Render for deployment

## Running Locally

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables:
   - Create a `.env` file with your NYT API key: `NYT_API_KEY=your_api_key`
6. Run the application: `python run.py`
7. Access the API documentation at `http://localhost:8000/docs`

## Testing

Run tests using pytest:
