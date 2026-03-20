from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class Character(Base):
    __tablename__ = "characters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    name_japanese = Column(String(100), nullable=True)
    anime_id = Column(Integer, ForeignKey("animes.id"), nullable=False)
    voice_actor = Column(String(100), nullable=True)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    anime = relationship("Anime", back_populates="characters")
    quotes = relationship("Quote", back_populates="character", cascade="all, delete-orphan")
