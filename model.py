from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

from database import Base


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    review_tags = relationship('ReviewTag', back_populates='tag')


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(2048))
    is_tagged = Column(Boolean, default=False)
    review_tags = relationship('ReviewTag', secondary='review_review_tags', back_populates='reviews')


class ReviewTag(Base):
    __tablename__ = 'review_tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_ai_tag = Column(Boolean, nullable=False, default=False)
    tag_id = Column(Integer, ForeignKey('tags.id'))
    tag = relationship('Tag', back_populates='review_tags')
    reviews = relationship('Review', secondary='review_review_tags', back_populates='review_tags')


class ReviewReviewTag(Base):
    __tablename__ = 'review_review_tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    review_id = Column(Integer, ForeignKey('reviews.id'))
    tag_id = Column(Integer, ForeignKey('review_tags.id'))
