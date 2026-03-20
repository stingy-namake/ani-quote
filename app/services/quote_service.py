from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_
from typing import List, Optional
from app.models import Quote, Character, Anime
from app.schemas.quote import QuoteCreate, QuoteUpdate, QuoteFilter


class QuoteService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, quote_id: int) -> Optional[Quote]:
        return self.db.query(Quote).options(
            joinedload(Quote.character).joinedload(Character.anime)
        ).filter(Quote.id == quote_id).first()
    
    def get_all(self, filters: QuoteFilter) -> tuple[List[Quote], int]:
        query = self.db.query(Quote).options(
            joinedload(Quote.character).joinedload(Character.anime)
        )
        
        # Apply filters
        if filters.anime_id:
            query = query.join(Quote.character).filter(
                Character.anime_id == filters.anime_id
            )
        
        if filters.character_id:
            query = query.filter(Quote.character_id == filters.character_id)
        
        if filters.search:
            search_filter = or_(
                Quote.content.ilike(f"%{filters.search}%"),
                Character.name.ilike(f"%{filters.search}%"),
                Anime.title.ilike(f"%{filters.search}%")
            )
            query = query.join(Quote.character).join(Character.anime).filter(search_filter)
        
        if filters.is_spoiler is not None:
            query = query.filter(Quote.is_spoiler == filters.is_spoiler)
        
        # Get total count
        total = query.count()
        
        # Pagination
        quotes = query.offset(filters.skip).limit(filters.limit).all()
        
        return quotes, total
    
    def get_random(self, anime_id: Optional[int] = None, 
                   character_id: Optional[int] = None) -> Optional[Quote]:
        query = self.db.query(Quote).options(
            joinedload(Quote.character).joinedload(Character.anime)
        )
        
        if anime_id:
            query = query.join(Quote.character).filter(Character.anime_id == anime_id)
        
        if character_id:
            query = query.filter(Quote.character_id == character_id)
        
        # Order by random (PostgreSQL specific)
        return query.order_by(func.random()).first()
    
    def create(self, quote_data: QuoteCreate) -> Quote:
        db_quote = Quote(**quote_data.model_dump())
        self.db.add(db_quote)
        self.db.commit()
        self.db.refresh(db_quote)
        return db_quote
    
    def update(self, quote_id: int, quote_data: QuoteUpdate) -> Optional[Quote]:
        db_quote = self.get_by_id(quote_id)
        if not db_quote:
            return None
        
        update_data = quote_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_quote, field, value)
        
        self.db.commit()
        self.db.refresh(db_quote)
        return db_quote
    
    def delete(self, quote_id: int) -> bool:
        db_quote = self.get_by_id(quote_id)
        if not db_quote:
            return False
        
        self.db.delete(db_quote)
        self.db.commit()
        return True
    
    def like_quote(self, quote_id: int) -> Optional[Quote]:
        db_quote = self.db.query(Quote).filter(Quote.id == quote_id).first()
        if not db_quote:
            return None
        
        db_quote.likes_count += 1
        self.db.commit()
        self.db.refresh(db_quote)
        return db_quote
