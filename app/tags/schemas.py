from app.core.schemas import BaseModel
from pydantic import constr

class TagCreateSchema(BaseModel):
    name: constr(max_length=50)