from model import *
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from fastapi import HTTPException, Query
from typing import List, Optional
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# TODO Please complete the FastAPI routing here


engine = create_engine('sqlite:///reviews.sqlite')


class ReviewModel(BaseModel):
    text: str


class TagModel(BaseModel):
    name: str


class TagId(BaseModel):
    value: int


class TagIdList(BaseModel):
    id_list: List[TagId]


@app.post("/reviews")
def create_review(review: ReviewModel):
    """
    Create a new review.

    Parameters:
        review (ReviewModel): The review object containing the text of the review.
    """
    with Session(engine) as db:
        db_review = Review(text=review.text)
        db.add(db_review)
        db.commit()
    return {"message": "Review created successfully"}


@app.post("/reviews/{review_id}/tags")
def add_tags_to_review(review_id: int, tag_ids: TagIdList):
    """
    Adds tags to a review.

    Parameters:
        review_id (int): The ID of the review.
        tag_ids (TagIdList): A list of tag IDs.
    """
    session = Session(engine)
    stmt = select(Review).where(Review.id == review_id)
    try:
        review = session.scalars(stmt).one()
        for tag in tag_ids.id_list:
            tag_id = tag.value
            stmt = select(Tag).where(Tag.id == tag_id)
            tag = session.scalars(stmt).one_or_none()
            if tag is None:
                session.close()
                raise HTTPException(status_code=404, detail="Tag not found")
            review.is_tagged = True
            stmt = select(Review_Review_Tag).where(
                Review_Review_Tag.review_id == review_id, Review_Review_Tag.review_tag_id == tag_id)
            review_review_tag = session.scalars(stmt).one_or_none()
            if review_review_tag is None:
                review_review_tag = Review_Review_Tag(
                    review_id=review_id, review_tag_id=tag_id)
                session.add(review_review_tag)
        session.commit()
    except:
        session.close()
        raise HTTPException(status_code=404, detail="Review not found")
    session.close()
    return {"message": "Tags added to review successfully"}


@app.get("/reviews")
def get_reviews(tag_id: Optional[List[int]] = Query(None), skip: int = 0, limit: int = 10):
    """
    Retrieves a list of reviews based on the specified criteria.

    Parameters:
        tag_id (Optional[List[int]]): A list of tag IDs to filter the reviews by. Defaults to None.
        skip (int): The number of reviews to skip. Defaults to 0.
        limit (int): The maximum number of reviews to retrieve. Defaults to 10.

    Returns:
        dict: A dictionary containing the retrieved reviews.
            - reviews (List[Review]): A list of Review objects.
    """
    with Session(engine) as session:
        if tag_id:
            stmt = select(Review).join(Review_Review_Tag, Review.id == Review_Review_Tag.review_id).join(
                Review_Tag, Review_Review_Tag.review_tag_id == Review_Tag.id).filter(Review_Tag.tag_id.in_(tag_id))
        else:
            stmt = select(Review)

        stmt = stmt.group_by(Review.id)
        stmt = stmt.order_by(Review.id).offset(skip).limit(limit)

        reviews = session.scalars(stmt).all()
    return {"reviews": reviews}


@app.post("/tags")
def create_tag(tag: TagModel):
    """
    Create a new tag in the database.

    Parameters:
        tag (TagModel): The tag object to be created.
    """
    with Session(engine) as session:
        db_tag = Tag(name=tag.name)
        session.add(db_tag)
        session.commit()
        review_tag = Review_Tag(tag_id=db_tag.id)
        session.add(review_tag)
        session.commit()
    return {"message": "Tag created successfully"}


@app.delete("/tags/{tag_id}")
def delete_tag(tag_id: int):
    """
    Deletes a tag with the specified tag_id.

    Parameters:
        tag_id (int): The ID of the tag to be deleted.
    """
    with Session(engine) as session:
        stmt = select(Tag).where(Tag.id == tag_id)
        tag = session.scalars(stmt).one_or_none()
        if tag is None:
            raise HTTPException(status_code=404, detail="Tag not found")

        stmt = select(Review_Tag).where(Review_Tag.tag_id == tag.id)
        review_tag = session.scalars(stmt).one_or_none()
        if review_tag is None:
            raise HTTPException(status_code=404, detail="ReviewTag not found")
        session.delete(review_tag)
        session.delete(tag)
        session.commit()
    return {"message": "Tag deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
