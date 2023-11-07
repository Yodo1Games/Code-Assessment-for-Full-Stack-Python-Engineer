from fastapi import APIRouter, Depends, Body, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.reviews.schemas import ReviewTagSchema
from app.reviews.domain import ReviewDomain
from typing import List

class ReviewRouter:
    def __init__(self, domain: ReviewDomain):
        self.__domain = domain

    @property
    def router(self):
        api_router = APIRouter(prefix='/reviews', tags=['reviews'])

        @api_router.post('/{review_id}/tags')
        def create(review_id: int, obj_in: ReviewTagSchema = Body(...), db: Session = Depends(get_db)):
            return self.__domain.create(review_id, db, obj_in)
        
        @api_router.get('')
        def get(page: int = Query(1, title="Page number"),  tags: List[int] = Query(None, title="List of tag IDs for conditional queries"), db: Session = Depends(get_db)):
            return self.__domain.get(page, tags, db)

        return api_router