from datetime import date, datetime
from typing import Optional, List
from fastapi import HTTPException

def validate_date_range(begin_date: Optional[date], end_date: Optional[date]):
    """
    Validate that the date range is logical (end date not before begin date)
    and that dates are not in the future.
    
    Raises HTTPException with appropriate error message if validation fails.
    """
    today = date.today()
    
    if begin_date and begin_date > today:
        raise HTTPException(
            status_code=400, 
            detail="Begin date cannot be in the future"
        )
    
    if end_date and end_date > today:
        raise HTTPException(
            status_code=400, 
            detail="End date cannot be in the future"
        )
    
    if begin_date and end_date and end_date < begin_date:
        raise HTTPException(
            status_code=400, 
            detail=f"End date ({end_date}) cannot be before begin date ({begin_date})"
        )

def validate_sort_parameter(sort: str, allowed_values: List[str] = None):
    """Validate that sort parameter is one of the allowed values"""
    if allowed_values is None:
        allowed_values = ["relevance", "newest", "oldest"]
        
    if sort.lower() not in allowed_values:
        raise HTTPException(
            status_code=400, 
            detail=f"Sort parameter must be one of: {', '.join(allowed_values)}"
        )

