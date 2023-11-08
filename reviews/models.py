from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(2048))
    is_tagged = Column(Boolean)
    #tags = relationship("Tag", back_populates="reviews")
    #tags = relationship('Tag', secondary='review_review_tags')

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

class ReviewTag(Base):
    __tablename__ = 'review_tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_ai_tag = Column(Boolean, nullable=False, default=False)
    tag_id = Column(Integer, ForeignKey('tags.id'))

class ReviewReviewTag(Base):
    __tablename__ = 'review_review_tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    review_id = Column(Integer, ForeignKey('reviews.id'))
    review_tag_id = Column(Integer, ForeignKey('review_tag.id'))