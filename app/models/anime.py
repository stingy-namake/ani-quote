from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class Anime(Base):
    __tablename__ = "animes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    title_japanese = Column(String(255), nullable=True)
    studio = Column(String(100), nullable=True)
    year = Column(Integer, nullable=True)
    genre = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    characters = relationship("Character", back_populates="anime", cascade="all, delete-orphan")
