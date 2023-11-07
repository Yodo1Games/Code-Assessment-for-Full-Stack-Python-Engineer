from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.tags.schemas import TagCreateSchema
from app.tags.domain import TagDomain

class TagRouter:
    def __init__(self, domain: TagDomain):
        self.__domain = domain

    @property
    def router(self):
        api_router = APIRouter(prefix='/tags', tags=['tags'])

        @api_router.post('')
        def create(obj_in: TagCreateSchema = Body(...), db: Session = Depends(get_db)):
            return self.__domain.create(db, obj_in)
        
        @api_router.delete('/{tag_id}')
        def delete(tag_id: int, db: Session = Depends(get_db)):
            return self.__domain.delete(db, tag_id)

        return api_router