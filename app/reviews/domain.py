from app.core.schemas import BaseModel
from sqlalchemy.orm import Session
from app.tags.schemas import TagCreateSchema
from app.reviews.repository import ReviewRepository

class ReviewDomain:
    """
    CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    **Parameters**

    * `repository`: A Repository class object of the Module

    """
    def __init__(self, repository:ReviewRepository) -> None:
        self.__repository = repository
    
    def create(self, id, db: Session, obj_in: TagCreateSchema):
        return self.__repository.create(id, db, obj_in=obj_in.dict())

    def get(self, page, tags, db: Session):
        return self.__repository.get(page, tags, db)