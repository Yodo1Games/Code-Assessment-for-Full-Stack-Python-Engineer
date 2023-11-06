from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel
from typing import List


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# TODO Please complete the FastAPI routing here

from fastapi import FastAPI, HTTPException, Query, Path, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import model
import schemas

# Initialize FastAPI app
app = FastAPI()

# Define your SQLAlchemy engine
engine = create_engine("sqlite:///reviews.db")

# Create models and tables based on your SQLAlchemy setup
model.Base.metadata.create_all(bind=engine)


# Dependency to get the database session
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


# Route to add tags to a review
@app.post("/reviews/{review_id}/tags")
async def add_tags_to_review(review_id: int, tags: List[str], db: Session = Depends(get_db)):
    # Query the database to find the review by ID
    review = db.query(model.Review).filter(model.Review.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    # Create Tag objects and associate them with the review
    for tag_name in tags:
        tag = model.Tag(name=tag_name)
        db.add(tag)
        db.commit()
        db.refresh(tag)

        review_tag = model.ReviewReviewTag(review_id=review_id, review_tag_id=tag.id)
        db.add(review_tag)
        db.commit()

    return {"message": "Tags added successfully"}


# Route to get reviews with paging and associated tags
@app.get("/reviews")
async def get_reviews(skip: int = Query(0, alias="page"), limit: int = Query(10), db: Session = Depends(get_db)):
    # Query reviews with pagination
    reviews = db.query(model.Review).offset(skip).limit(limit).all()

    # Fetch associated tags for each review
    response = []
    for review in reviews:
        tags = db.query(model.Tag).join(model.ReviewTag).filter(model.ReviewTag.tag_id == model.Tag.id,
                                                                  model.ReviewTag.review_id == review.id).all()
        response.append({"review": review, "tags": tags})

    return response


# Route to create a new tag
@app.post("/tags")
async def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    new_tag = model.Tag(**tag.model_dump())
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag

@app.post("/create-review")
async def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    new_review = model.Review(**review.model_dump())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

# Route to delete a tag by ID
@app.delete("/tags/{tag_id}")
async def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(model.Tag).filter(model.Tag.id == tag_id).first()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    db.delete(tag)
    db.commit()

    # Also delete associated review_tag entries
    review_tags = db.query(model.ReviewTag).filter(model.ReviewTag.tag_id == tag_id).all()
    for review_tag in review_tags:
        db.delete(review_tag)

    db.commit()

    return {"message": "Tag deleted successfully"}

