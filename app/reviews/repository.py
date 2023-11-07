from app.reviews.models import Reviews, ReviewTag, ReviewReviewTag
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.tags.models import Tag

class ReviewRepository:
    
    def create(self, id, db: Session, obj_in: None):      
        review = db.query(Reviews).filter(Reviews.id == id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        tags = db.query(Tag).filter(Tag.id.in_(obj_in['tags'])).all()
        if not tags:
            raise HTTPException(status_code=404, detail="Tags not found")

        for tag in tags:
            review_tag = ReviewTag(is_ai_tag=False, tag_id=tag.id, review_id=review.id)
            db.add(review_tag)

        review.is_tagged = True
        db.commit()
        return {"message": "Tags added successfully"}
    
    def get(self, page, tags, db: Session):
        query = db.query(Reviews)
        if tags:
            query = query.join(Reviews.tags).filter(Tag.id.in_(tags))
        
        reviews = query.offset((page - 1) * 10).limit(10).all()
        return reviews