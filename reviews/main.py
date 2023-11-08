from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/reviews/{review_id}/tags/{tag_id}", response_model=schemas.ReviewBase)
def create_review(review_id:int, tag_id:int, review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.add_tag_to_review(review_id=review_id, tag_id=tag_id, db=db, review=review)

@app.post("/tags/", response_model=schemas.TagBase)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    return crud.create_tag(db=db, tag=tag)

@app.delete("/tags/{tag_id}", response_model=schemas.TagBase)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    return crud.delete_tag(db=db, tag_id=tag_id)


@app.get("/reviews/", response_model=List[schemas.Review])
def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_reviews(db, skip=skip, limit=limit)
    return users

