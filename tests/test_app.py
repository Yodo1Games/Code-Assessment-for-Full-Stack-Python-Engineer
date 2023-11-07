import model as models
import schema as schemas
import curd
from . import client, db, test_db


def test_create_tag(test_db):
    response = client.post("/tags", json={"name": "test tag"})
    assert response.status_code == 200
    assert response.json()["name"] == "test tag"


def test_add_tag_to_review(test_db):
    review = curd.create_review(db, schemas.Review(**dict(id=1, text="This is a test review", is_tagged=False, tags=[])))
    assert len(review.review_tags) == 0

    response = client.post(f"/reviews/{review.id}/tags", json={"name": "test tag"})
    assert response.status_code == 200

    db.refresh(review)
    assert len(review.review_tags) == 1
    tag = db.query(models.Tag).filter(models.Tag.id == review.review_tags[0].tag_id).first()
    assert tag.name == 'test tag'


def test_read_reviews(test_db):
    curd.create_review(db, schemas.Review(**dict(id=1, text="This is a test review", is_tagged=False, tags=[])))
    response = client.get("/reviews")
    assert response.status_code == 200
    assert len(curd.get_reviews(db)) == 1


def test_delete_tag(test_db):
    response = client.delete("/tags/1")
    assert response.status_code == 404

    tag = curd.create_tag(db, schemas.TagCreate(**dict(name='tag1')))
    review_tag = curd.create_review_tag(db, schemas.ReviewTagCreate(**dict(is_ai_tag=False, tag_id=tag.id)))

    tag = db.query(models.ReviewTag).filter(models.ReviewTag.tag_id == tag.id).first()
    assert tag.id == review_tag.id

    response = client.delete(f"/tags/{tag.id}")
    assert response.status_code == 200

    # review tag should be removed when tag is removed.
    tag = db.query(models.ReviewTag).filter(models.ReviewTag.tag_id == tag.id).first()
    assert tag is None
