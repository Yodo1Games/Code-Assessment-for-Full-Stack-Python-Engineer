from app.tags.models import Tag
from sqlalchemy.orm import Session
from fastapi import HTTPException

class TagRepository:
    def __init__(self):
        """
        CRUD object with default methods to Create Delete.

        **Parameters**

        * `model`: A SQLAlchemy model class
        """
        self.model = Tag
    
    def create(self, db: Session, obj_in: None) -> Tag:
        """
        Create an object.
        Args:
            db: Session
            obj_in: ModelCreateSchemaObject

        Returns:
            ModelType
        """
      
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        try:
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=403, detail=str(e))
    
    def delete(self, db: Session, id: int) -> Tag:
        """
        Delete an object.
        Args:
            db: Session
            id: item id

        Returns:
            ModelType
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        try:
            db.commit()
            return obj
        except Exception as e:
            db.rollback()
            return None
