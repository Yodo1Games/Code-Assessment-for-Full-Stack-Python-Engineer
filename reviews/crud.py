from sqlalchemy.orm import Session

from . import models, schemas


def create_review(db: Session, review: schemas.ReviewCreate):
    db_item = models.Review(**review.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def create_tag(db: Session, tag: schemas.TagCreate):
    db_item = models.Tag(**tag.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Delete a tag by ID
def delete_tag(db: Session, tag_id: int):
    db_item = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return db_item
    return None

# Add a Tag to a specified Review
def add_tag_to_review(db: Session, review_id: int, tag_id: int):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()

    if review and tag:
        review_tag = models.ReviewTag(is_ai_tag=False, tag_id=tag_id)
        db.add(review_tag)

        review_review_tag = models.ReviewReviewTag(review_id=review_id, review_tag_id=review_tag.id)
        db.add(review_review_tag)

        db.commit()
        
        return review
    return None