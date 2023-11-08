import datetime
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Date, Float, Boolean
from sqlalchemy.orm import relationship
from app.core.base import Base

class Reviews(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    text = Column(String(2048))
    is_tagged = Column(Boolean)
    review_review_tag = relationship('ReviewReviewTag', back_populates='reviews')


class ReviewTag(Base):
    __tablename__ = 'review_tag'

    id = Column(Integer, primary_key=True)
    is_ai_tag = Column(Boolean, default=False)
    tag_id = Column(Integer, ForeignKey('tags.id'))
    tag = relationship('Tag', back_populates='review_tag')
    review_review_tag = relationship('ReviewReviewTag', back_populates='review_tag')


class ReviewReviewTag(Base):
    __tablename__ = 'review_review_tag'

    id = Column(Integer, primary_key=True)
    review_id = Column(Integer, ForeignKey('reviews.id'))
    reviews = relationship('Reviews', back_populates='review_review_tag')
    review_tag_id = Column(Integer, ForeignKey('review_tag.id'))
    review_tag = relationship('ReviewTag', back_populates='review_review_tag')