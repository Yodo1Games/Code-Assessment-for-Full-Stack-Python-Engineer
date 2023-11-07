
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

# Define the SQLite database URL (you can adjust the path as needed)
DATABASE_URL = "sqlite:///reviews.db"

# Create a database engine
engine = create_engine(DATABASE_URL)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base for declarative class
Base = declarative_base()

# Define the 'tags' table


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

# Define the 'review_tag' table


class ReviewTag(Base):
    __tablename__ = "review_tags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_ai_tag = Column(Boolean, nullable=False, default=False)
    tag_id = Column(Integer, ForeignKey("tags.id"))

# Define the 'reviews' table


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(2048))
    is_tagged = Column(Boolean, default=False)
    review_tags = relationship("ReviewTag", secondary="review_review_tags")

# Define the 'review_review_tags' table


class ReviewReviewTag(Base):
    __tablename__ = "review_review_tags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    review_id = Column(Integer, ForeignKey("reviews.id"))
    review_tag_id = Column(Integer, ForeignKey("review_tags.id"))


if __name__ == "__main__":
    # Create the tables in the database
    Base.metadata.create_all(bind=engine)
