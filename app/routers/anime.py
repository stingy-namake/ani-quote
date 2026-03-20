from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models import Anime, Character, Quote
from app.schemas.anime import AnimeCreate, AnimeUpdate, AnimeInDB, AnimeWithStats

router = APIRouter(prefix="/anime", tags=["anime"])


@router.get("/", response_model=List[AnimeWithStats])
def get_all_anime(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all anime with statistics."""
    anime_list = db.query(Anime).offset(skip).limit(limit).all()
    
    result = []
    for anime in anime_list:
        char_count = db.query(Character).filter(Character.anime_id == anime.id).count()
        quote_count = db.query(Quote).join(Character).filter(Character.anime_id == anime.id).count()
        
        anime_dict = {
            **anime.__dict__,
            "character_count": char_count,
            "quote_count": quote_count
        }
        result.append(anime_dict)
    
    return result


@router.get("/{anime_id}", response_model=AnimeWithStats)
def get_anime(anime_id: int, db: Session = Depends(get_db)):
    """Get a specific anime by ID."""
    anime = db.query(Anime).filter(Anime.id == anime_id).first()
    
    if not anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    
    char_count = db.query(Character).filter(Character.anime_id == anime.id).count()
    quote_count = db.query(Quote).join(Character).filter(Character.anime_id == anime.id).count()
    
    return {
        **anime.__dict__,
        "character_count": char_count,
        "quote_count": quote_count
    }


@router.post("/", response_model=AnimeInDB, status_code=status.HTTP_201_CREATED)
def create_anime(anime: AnimeCreate, db: Session = Depends(get_db)):
    """Create a new anime entry."""
    db_anime = Anime(**anime.model_dump())
    db.add(db_anime)
    db.commit()
    db.refresh(db_anime)
    return db_anime


@router.put("/{anime_id}", response_model=AnimeInDB)
def update_anime(anime_id: int, anime: AnimeUpdate, db: Session = Depends(get_db)):
    """Update an existing anime."""
    db_anime = db.query(Anime).filter(Anime.id == anime_id).first()
    
    if not db_anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    
    update_data = anime.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_anime, field, value)
    
    db.commit()
    db.refresh(db_anime)
    return db_anime


@router.delete("/{anime_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_anime(anime_id: int, db: Session = Depends(get_db)):
    """Delete an anime and all associated characters/quotes."""
    db_anime = db.query(Anime).filter(Anime.id == anime_id).first()
    
    if not db_anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    
    db.delete(db_anime)
    db.commit()
    return None
