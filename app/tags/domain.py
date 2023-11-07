from app.core.schemas import BaseModel
from sqlalchemy.orm import Session
from app.tags.schemas import TagCreateSchema
from app.tags.repository import TagRepository

class TagDomain:
    """
    CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    **Parameters**

    * `repository`: A Repository class object of the Module

    """
    def __init__(self, repository:TagRepository) -> None:
        self.__repository = repository
    
    def create(self, db: Session, obj_in: TagCreateSchema):
        return self.__repository.create(db, obj_in=obj_in.dict())

    def delete(self, db: Session, id: int):
        return self.__repository.delete(db, id=id)