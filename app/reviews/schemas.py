from app.core.schemas import BaseModel
from pydantic import conint


class ReviewTagSchema(BaseModel):
    tags: list[conint(ge=0)]