# TODO Please complete the Table definition here
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Create an SQLite database named "reviews"
engine = create_engine("sqlite:///reviews.db")

# Create a base class for your models
Base = declarative_base()

# Define the "reviews" table
# Define the "reviews" table
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(2048))
    is_tagged = Column(Boolean)

    # Relationship with ReviewTag
    review_tags = relationship("ReviewTag", back_populates="review")

# Define the "tags" table
class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    # Relationship with ReviewTag
    review_tags = relationship("ReviewTag", back_populates="tag")

# Define the "review_tags" table
class ReviewTag(Base):
    __tablename__ = "review_tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    is_ai_tag = Column(Boolean, nullable=False, default=False)
    tag_id = Column(Integer, ForeignKey("tags.id"))
    review_id = Column(Integer, ForeignKey("reviews.id"))

    # Relationships with Review and Tag
    review = relationship("Review", back_populates="review_tags")
    tag = relationship("Tag", back_populates="review_tags")

# Define the "review_review_tags" table
class ReviewReviewTag(Base):
    __tablename__ = "review_review_tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    review_id = Column(Integer, ForeignKey("reviews.id"))
    review_tag_id = Column(Integer, ForeignKey("review_tags.id"))

    # Relationships with Review and ReviewTag
    review = relationship("Review")
    review_tag = relationship("ReviewTag")


# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# You can now use the session to add, query, or modify data in your SQLite database.

# Don't forget to commit your changes and close the session when you're done.
session.commit()
session.close()
