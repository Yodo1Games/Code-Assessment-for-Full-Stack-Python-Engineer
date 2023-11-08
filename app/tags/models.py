from sqlalchemy import Column, Integer, String
from app.core.base import Base
from sqlalchemy.orm import relationship

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    review_tag = relationship('ReviewTag', back_populates='tag')
 