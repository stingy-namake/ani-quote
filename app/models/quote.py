from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Quote(Base):
    __tablename__ = "quotes"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(1000), nullable=False)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    episode = Column(Integer, nullable=True)
    context = Column(String(500), nullable=True)  # Scene description
    is_spoiler = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    likes_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    character = relationship("Character", back_populates="quotes")
    
    @property
    def anime(self):
        return self.character.anime if self.character else None
