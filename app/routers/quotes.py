from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.quote import (
    QuoteCreate, QuoteUpdate, QuoteInDB, QuoteWithDetails, 
    QuoteFilter, RandomQuoteRequest
)
from app.services.quote_service import QuoteService

router = APIRouter(prefix="/quotes", tags=["quotes"])


@router.get("/", response_model=dict)
def get_quotes(
    anime_id: Optional[int] = None,
    character_id: Optional[int] = None,
    search: Optional[str] = None,
    is_spoiler: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all quotes with optional filtering and pagination."""
    filters = QuoteFilter(
        anime_id=anime_id,
        character_id=character_id,
        search=search,
        is_spoiler=is_spoiler,
        skip=skip,
        limit=limit
    )
    
    service = QuoteService(db)
    quotes, total = service.get_all(filters)
    
    # Convert to response schema with details
    results = []
    for quote in quotes:
        q_dict = {
            **quote.__dict__,
            "character_name": quote.character.name if quote.character else None,
            "anime_title": quote.character.anime.title if quote.character and quote.character.anime else None,
            "anime_id": quote.character.anime.id if quote.character and quote.character.anime else None
        }
        results.append(q_dict)
    
    return {
        "data": results,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.get("/random", response_model=QuoteWithDetails)
def get_random_quote(
    anime_id: Optional[int] = None,
    character_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get a random quote, optionally filtered by anime or character."""
    service = QuoteService(db)
    quote = service.get_random(anime_id=anime_id, character_id=character_id)
    
    if not quote:
        raise HTTPException(status_code=404, detail="No quotes found")
    
    return {
        **quote.__dict__,
        "character_name": quote.character.name if quote.character else None,
        "anime_title": quote.character.anime.title if quote.character and quote.character.anime else None,
        "anime_id": quote.character.anime.id if quote.character and quote.character.anime else None
    }


@router.get("/{quote_id}", response_model=QuoteWithDetails)
def get_quote(quote_id: int, db: Session = Depends(get_db)):
    """Get a specific quote by ID."""
    service = QuoteService(db)
    quote = service.get_by_id(quote_id)
    
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    return {
        **quote.__dict__,
        "character_name": quote.character.name if quote.character else None,
        "anime_title": quote.character.anime.title if quote.character and quote.character.anime else None,
        "anime_id": quote.character.anime.id if quote.character and quote.character.anime else None
    }


@router.post("/", response_model=QuoteInDB, status_code=status.HTTP_201_CREATED)
def create_quote(quote: QuoteCreate, db: Session = Depends(get_db)):
    """Create a new quote."""
    service = QuoteService(db)
    return service.create(quote)


@router.put("/{quote_id}", response_model=QuoteInDB)
def update_quote(quote_id: int, quote: QuoteUpdate, db: Session = Depends(get_db)):
    """Update an existing quote."""
    service = QuoteService(db)
    updated = service.update(quote_id, quote)
    
    if not updated:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    return updated


@router.delete("/{quote_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quote(quote_id: int, db: Session = Depends(get_db)):
    """Delete a quote."""
    service = QuoteService(db)
    deleted = service.delete(quote_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    return None


@router.post("/{quote_id}/like", response_model=QuoteInDB)
def like_quote(quote_id: int, db: Session = Depends(get_db)):
    """Increment likes for a quote."""
    service = QuoteService(db)
    quote = service.like_quote(quote_id)
    
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    return quote
