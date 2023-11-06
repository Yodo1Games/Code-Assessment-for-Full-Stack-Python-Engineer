# TODO Please complete the Table definition here
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    text = Column(String(2048))
    is_tagged = Column(Boolean)

    review_review_tags = relationship('Review_Review_Tag', backref='review')

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    review_tags = relationship('Review_Tag', backref='tag')

class Review_Tag(Base):
    __tablename__ = 'review_tag'

    id = Column(Integer, primary_key=True)
    is_ai_tag = Column(Boolean, default=False, nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.id'))

    review_review_tags = relationship('Review_Review_Tag', backref='review_tag')

class Review_Review_Tag(Base):
    __tablename__ = 'review_review_tag'

    id = Column(Integer, primary_key=True)
    review_id = Column(Integer, ForeignKey('reviews.id'))
    review_tag_id = Column(Integer, ForeignKey('review_tag.id'))


if __name__ == '__main__':
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///reviews.sqlite')
    Base.metadata.create_all(engine)
