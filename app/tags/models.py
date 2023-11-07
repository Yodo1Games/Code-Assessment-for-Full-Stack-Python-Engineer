from sqlalchemy import Column, Integer, String
from app.core.base import Base

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
 