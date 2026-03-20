from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CharacterBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    name_japanese: Optional[str] = Field(None, max_length=100)
    voice_actor: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CharacterCreate(CharacterBase):
    anime_id: int


class CharacterUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    name_japanese: Optional[str] = None
    voice_actor: Optional[str] = None
    description: Optional[str] = None


class CharacterInDB(CharacterBase):
    id: int
    anime_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class CharacterWithAnime(CharacterInDB):
    anime_title: Optional[str] = None
    quote_count: int = 0
