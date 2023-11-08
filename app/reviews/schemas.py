from app.core.schemas import BaseModel
from pydantic import conint
from typing import List

class ReviewTagSchema(BaseModel):
    tags: list[conint(ge=0)]


class TagResponse(BaseModel):
    id: int
    name: str

class ReviewTagResponse(BaseModel):
    id: int
    is_ai_tag: bool
    tag: TagResponse

class ReviewResponse(BaseModel):
    id: int
    text: str
    is_tagged: bool
    review_review_tag: List[ReviewTagResponse]