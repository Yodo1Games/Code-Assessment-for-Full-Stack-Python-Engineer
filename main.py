# TODO Please complete the FastAPI routing here

from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Path, Query, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Tag, Review, ReviewTag
from pydantic import BaseModel
app = FastAPI()

# Define the database URL
DATABASE_URL = "sqlite:///reviews.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)


class ReviewResponse(BaseModel):
    id: int
    text: str
    is_tagged: bool


class TagResponse(BaseModel):
    id: int
    name: str


@app.post("/reviews/{review_id}/tags", response_model=ReviewResponse)
def add_tag_to_review(
    review_id: int = Path(title="The ID of the review"),
    tag_ids: list[int] = Query(title="List of Tag IDs to add to the review"),
):
    # Add tags to a review with the specified ID
    review = SessionLocal.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    for tag_id in tag_ids:
        tag = SessionLocal.query(Tag).filter(Tag.id == tag_id).first()
        if tag:
            review_tag = ReviewTag(review_id=review.id, tag_id=tag.id)
            SessionLocal.add(review_tag)

    SessionLocal.commit()
    return review


@app.get("/reviews", response_model=list[ReviewResponse])
def get_reviews_with_tags(
    page: int = Query(1, title="Page number", ge=1),
    limit: int = Query(10, title="Items per page", le=100),
    tag_ids: list[int] = Query(None, title="List of Tag IDs for filtering"),
):
    # Get a list of reviews with optional tag filtering
    reviews = SessionLocal.query(Review).all()

    if tag_ids:
        reviews = [review for review in reviews if any(
            tag.id in tag_ids for tag in review.tags)]

    return reviews


@app.post("/tags", response_model=None)
def create_tag(tag: Tag):
    new_tag = Tag(**tag.dict())
    SessionLocal.add(new_tag)
    SessionLocal.commit()
    return new_tag



@app.delete("/tags/{tag_id}")
def delete_tag(tag_id: int):
    
    session = SessionLocal()
    
    try:
        tag = session.query(Tag).filter(Tag.id == tag_id).first()
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        session.delete(tag)
        session.query(ReviewTag).filter(ReviewTag.tag_id == tag_id).delete(synchronize_session=False)
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

    return {"message": "Tag deleted successfully"}