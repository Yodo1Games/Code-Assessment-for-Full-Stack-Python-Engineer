from sqlalchemy.orm import Session

import model as models
import schema as schemas


def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()


def delete_tag_and_tag_reviews(db: Session, tag: schemas.Tag):
    db_review_tags = db.query(models.ReviewTag).filter(models.ReviewTag.tag_id == tag.id).all()
    for db_review_tag in db_review_tags:
        db.delete(db_review_tag)

    db.delete(tag)
    db.commit()


def create_review_tag(db: Session, review_tag: schemas.ReviewTagCreate):
    db_review_tag = models.ReviewTag(is_ai_tag=review_tag.is_ai_tag, tag_id=review_tag.tag_id)
    db.add(db_review_tag)
    db.commit()
    db.refresh(db_review_tag)
    return db_review_tag


def create_review(db: Session, review: schemas.Review):
    db_review = models.Review(text=review.text, is_tagged=review.is_tagged)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def add_review_tag_to_review(db: Session, review: schemas.Review, review_tag: schemas.ReviewTag):
    review.review_tags.append(review_tag)
    db.commit()
    db.refresh(review)
    return review


def get_reviews(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Review).offset(skip).limit(limit).all()
