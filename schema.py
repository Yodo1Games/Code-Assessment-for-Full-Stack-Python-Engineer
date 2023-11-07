from pydantic import BaseModel
from typing import List, Optional


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True


class ReviewTagBase(BaseModel):
    is_ai_tag: bool
    tag_id: int


class ReviewTagCreate(ReviewTagBase):
    pass


class ReviewTag(ReviewTagBase):
    id: int

    class Config:
        orm_mode = True


class ReviewBase(BaseModel):
    text: str
    is_tagged: bool


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
    tags: List[ReviewTag] = []

    class Config:
        orm_mode = True
