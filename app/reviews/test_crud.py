from app.core.test_app import TestApp, override_get_db
from app.tags.test_crud import TestTag
from app.reviews.models import Reviews

OBJECT_ID = 0

class TestReview(TestApp):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.module = 'reviews'

    def test_1_add_review_tags(self):
        TestTag.test_1_create_tags(self)
        review_data = {
            "text":"Dummy Text",
            "is_tagged": False
        }
        review = Reviews(**review_data)
        db = override_get_db()
        db.add(review)
        db.commit()
        db.refresh()
        data = {
            "tags": [1]
        }
        response = self.client.post("/api/v1/reviews/1/tags", json=data)
        self.assertEqual(response.status_code, 200)

    def test_2_get_reviews(self):
        response = self.client.delete(f"/api/v1/reviews")
        self.assertEqual(response.status_code, 200)
