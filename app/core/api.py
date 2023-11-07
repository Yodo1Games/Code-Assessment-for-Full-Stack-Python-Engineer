from fastapi import APIRouter
from app.tags.router import TagRouter
from app.tags.domain import TagDomain
from app.tags.repository import TagRepository
from app.reviews.repository import ReviewRepository
from app.reviews.domain import ReviewDomain
from app.reviews.router import ReviewRouter

api_router = APIRouter()
tag_repository = TagRepository()
tag_domain = TagDomain(tag_repository)
tag_router = TagRouter(tag_domain)
api_router.include_router(tag_router.router)


review_tag_repository = ReviewRepository()
review_tag_domain = ReviewDomain(review_tag_repository)
review_tag_router = ReviewRouter(review_tag_domain)
api_router.include_router(review_tag_router.router)
