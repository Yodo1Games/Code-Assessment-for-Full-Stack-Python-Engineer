from pydantic import BaseModel

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class ReviewBase(BaseModel):
    text: str
    is_tagged: bool

class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True

class ReviewCreate(ReviewBase):
    pass
