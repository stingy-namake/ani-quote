from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Character, Quote
from app.schemas.character import CharacterCreate, CharacterUpdate, CharacterInDB, CharacterWithAnime

router = APIRouter(prefix="/characters", tags=["characters"])


@router.get("/", response_model=List[CharacterWithAnime])
def get_all_characters(anime_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all characters, optionally filtered by anime."""
    query = db.query(Character)
    
    if anime_id:
        query = query.filter(Character.anime_id == anime_id)
    
    characters = query.offset(skip).limit(limit).all()
    
    result = []
    for char in characters:
        quote_count = db.query(Quote).filter(Quote.character_id == char.id).count()
        
        char_dict = {
            **char.__dict__,
            "anime_title": char.anime.title if char.anime else None,
            "quote_count": quote_count
        }
        result.append(char_dict)
    
    return result


@router.get("/{character_id}", response_model=CharacterWithAnime)
def get_character(character_id: int, db: Session = Depends(get_db)):
    """Get a specific character by ID."""
    character = db.query(Character).filter(Character.id == character_id).first()
    
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    quote_count = db.query(Quote).filter(Quote.character_id == character.id).count()
    
    return {
        **character.__dict__,
        "anime_title": character.anime.title if character.anime else None,
        "quote_count": quote_count
    }


@router.post("/", response_model=CharacterInDB, status_code=status.HTTP_201_CREATED)
def create_character(character: CharacterCreate, db: Session = Depends(get_db)):
    """Create a new character."""
    db_character = Character(**character.model_dump())
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character


@router.put("/{character_id}", response_model=CharacterInDB)
def update_character(character_id: int, character: CharacterUpdate, db: Session = Depends(get_db)):
    """Update an existing character."""
    db_character = db.query(Character).filter(Character.id == character_id).first()
    
    if not db_character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    update_data = character.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_character, field, value)
    
    db.commit()
    db.refresh(db_character)
    return db_character


@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_character(character_id: int, db: Session = Depends(get_db)):
    """Delete a character and all their quotes."""
    db_character = db.query(Character).filter(Character.id == character_id).first()
    
    if not db_character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    db.delete(db_character)
    db.commit()
    return None
