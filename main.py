from fastapi import FastAPI, Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import Base, engine, SessionLocal
import schema as schemas
import model as models
import curd

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/reviews/{review_id}/tags", response_model=schemas.Review)
def add_tag_to_review(review_id: int, tag: schemas.TagCreate, db: Session = Depends(get_db)):
    # Implement the logic to add a tag to a review
    # You'll need to look up the review by id, create a new tag, and associate it with the review
    # If the review doesn't exist, raise an HTTPException with status code 404
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    db_tag = models.Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)

    db_review_tag = models.ReviewTag(is_ai_tag=False, tag_id=db_tag.id)
    db.add(db_review_tag)
    db.commit()
    db.refresh(db_review_tag)

    db_review.review_tags.append(db_review_tag)
    db.commit()
    db.refresh(db_review)

    return db_review


@app.get("/reviews", response_model=List[schemas.Review])
def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return curd.get_reviews(db, skip, limit)


@app.post("/tags", response_model=schemas.Tag)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    return curd.create_tag(db, tag)


@app.delete("/tags/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = curd.get_tag(db, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    curd.delete_tag_and_tag_reviews(db, db_tag)
