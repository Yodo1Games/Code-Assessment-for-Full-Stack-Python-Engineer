from app.core.test_app import TestApp, override_get_db
from app.reviews.models import Reviews

OBJECT_ID = 0

class TestCrud(TestApp):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

    def test_1_create_tags(self):
        data = {
            "name": "test"
        }
        response = self.client.post("/api/v1/tags", json=data)
        self.assertEqual(response.status_code, 200)
        global OBJECT_ID
        OBJECT_ID = response.json()['id']


    def test_2_delete_tag(self):
        response = self.client.delete(f"/api/v1/tags/{OBJECT_ID}")
        self.assertEqual(response.status_code, 200)

    def test_3_add_review_tags(self):
        self.test_1_create_tags()
        review_data = {
            "text":"Dummy Text",
            "is_tagged": False
        }
        review = Reviews(**review_data)
        db = next(override_get_db())
        db.add(review)
        db.commit()
        db.refresh(review)
        data = {
            "tags": [1]
        }
        response = self.client.post("/api/v1/reviews/1/tags", json=data)
        self.assertEqual(response.status_code, 200)

    def test_4_get_reviews(self):
        response = self.client.get(f"/api/v1/reviews")
        self.assertEqual(response.status_code, 200)
