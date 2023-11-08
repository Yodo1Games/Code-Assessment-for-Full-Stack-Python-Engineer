from app.reviews.models import Reviews, ReviewTag, ReviewReviewTag
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app.tags.models import Tag

class ReviewRepository:
    
    def create(self, id, db: Session, obj_in: None):
        """
            Create a new review with associated tags in the database.

            Args:
            - id (int): The ID of the review to associate tags with.
            - db (Session): The database session to use.
            - obj_in (dict): Dictionary containing information for creating tags.

            Returns:
            - Review: The created or updated review object.

            Raises:
            - HTTPException: If the review or tags are not found.

            Usage Example:
            ```
            your_instance.create(id=1, db=session_instance, obj_in={"tags": [1, 2]})
            ```

        """
        try:
            review = db.query(Reviews).filter(Reviews.id == id).first()
            if not review:
                raise HTTPException(status_code=404, detail="Review not found")

            tags = db.query(Tag).filter(Tag.id.in_(obj_in['tags'])).all()
            if not tags:
                raise HTTPException(status_code=404, detail="Tags not found")

            for tag in tags:
                review_tag = ReviewTag(is_ai_tag=False, tag_id=tag.id)
                db.add(review_tag)

                review_review_tag = ReviewReviewTag(review_id=review.id, review_tag_id=review_tag.id)
                db.add(review_review_tag)

            review.is_tagged = True
            db.commit()
            return review
        
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=403, detail=str(e))
        
    

    def get(self, page, tags, db: Session):
        """
            Retrieve a paginated list of reviews with associated tags based on optional tag filtering.

            Args:
            - page (int): The page number for pagination.
            - tags (List[int]): Optional list of tag IDs for filtering reviews.
            - db (Session): The database session to use.

            Returns:
            - List[Review]: A paginated list of reviews with associated tags.

            Usage Example:
            ```
            reviews_list = your_instance.get(page=1, tags=[1, 2], db=session_instance)
            ```

        """

        skip = (page - 1) * 10

        query = (
            db.query(Reviews)
            .options(joinedload(Reviews.review_review_tag)
                    .joinedload(ReviewReviewTag.review_tag)
                    .joinedload(ReviewTag.tag))
            .offset(skip)
            .limit(10)
        )

        if tags:
            query = query.filter(ReviewTag.tag_id.in_(tags))

        reviews = query.all()

        return reviews