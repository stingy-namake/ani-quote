from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class AnimeBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    title_japanese: Optional[str] = Field(None, max_length=255)
    studio: Optional[str] = Field(None, max_length=100)
    year: Optional[int] = Field(None, ge=1900, le=2100)
    genre: Optional[str] = Field(None, max_length=100)


class AnimeCreate(AnimeBase):
    pass


class AnimeUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    title_japanese: Optional[str] = None
    studio: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None


class AnimeInDB(AnimeBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class AnimeWithStats(AnimeInDB):
    character_count: int = 0
    quote_count: int = 0
