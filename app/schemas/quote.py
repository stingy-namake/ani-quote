from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class QuoteBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)
    episode: Optional[int] = Field(None, ge=1)
    context: Optional[str] = Field(None, max_length=500)
    is_spoiler: bool = False


class QuoteCreate(QuoteBase):
    character_id: int


class QuoteUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=1000)
    episode: Optional[int] = None
    context: Optional[str] = None
    is_spoiler: Optional[bool] = None


class QuoteInDB(QuoteBase):
    id: int
    character_id: int
    is_verified: bool
    likes_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class QuoteWithDetails(QuoteInDB):
    character_name: Optional[str] = None
    anime_title: Optional[str] = None
    anime_id: Optional[int] = None


class QuoteFilter(BaseModel):
    anime_id: Optional[int] = None
    character_id: Optional[int] = None
    search: Optional[str] = None
    is_spoiler: Optional[bool] = None
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)


class RandomQuoteRequest(BaseModel):
    anime_id: Optional[int] = None
    character_id: Optional[int] = None
