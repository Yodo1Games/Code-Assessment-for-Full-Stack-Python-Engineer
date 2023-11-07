# TODO Please complete the test case here
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from main import app
from model import Review, Review_Review_Tag, Tag, Review_Tag

engine = create_engine('sqlite:///reviews.sqlite')

client = TestClient(app)

class TestFastAPIApp:

    def setup_method(self):
        self.db = Session(engine)
        self.db.query(Review).delete()
        self.db.query(Review_Tag).delete()
        self.db.query(Tag).delete()
        self.db.query(Review_Review_Tag).delete()
        self.db.commit()

    def teardown_method(self):
        self.db.query(Review).delete()
        self.db.query(Review_Tag).delete()
        self.db.query(Tag).delete()
        self.db.query(Review_Review_Tag).delete()
        self.db.commit()
        self.db.close()

    def test_create_tag(self):
        response = client.post("/tags", json={"name": "Test Tag"})
        assert response.status_code == 200

    def test_delete_tag(self):
        response = client.post("/tags", json={"name": "Test Tag"})
        response = client.delete(f"/tags/1")
        assert response.status_code == 200

    def test_create_review(self):
        response = client.post("/reviews", json={"text": "Test Review1"})
        assert response.status_code == 200

    def test_add_tag_to_non_existent_review(self):
        client.post("/tags", json={"name": "Test Tag"})
        response = client.post("/reviews/999/tags", json = {"id_list": [{"value": 1} ]})
        assert response.status_code == 404

    def test_add_tag_to_review(self):
        client.post("/reviews", json={"text": "Test Review1"})
        client.post("/tags", json={"name": "Test Tag1"})
        client.post("/tags", json={"name": "Test Tag2"})
        response = client.post(f"/reviews/1/tags", json = {"id_list": [{"value": 1} , {"value": 2} ]})
        assert response.status_code == 200
       
    def test_get_reviews_with_no_data(self):
        client.post("/reviews", json={"text": "Test Review1"})
        response = client.get("/reviews")
        assert response.status_code == 200
        assert response.json() == {"reviews": [{'id': 1, 'is_tagged': False, 'text': 'Test Review1'}]}
    
    def test_get_reviews_with_tag(self):
        client.post("/reviews", json={"text": "Test Review1"})
        client.post("/reviews", json={"text": "Test Review2"})
        client.post("/reviews", json={"text": "Test Review3"})
        client.post("/tags", json={"name": "Test Tag1"})
        client.post("/tags", json={"name": "Test Tag2"})
        client.post("/tags", json={"name": "Test Tag3"})
        client.post(f"/reviews/1/tags", json = {"id_list": [{"value": 1} ]})
        client.post(f"/reviews/2/tags", json = {"id_list": [{"value": 1} , {"value": 2} ]})
        client.post(f"/reviews/3/tags", json = {"id_list": [{"value": 1} , {"value": 2} , {"value": 3} ]})

        response = client.get("/reviews", params={"tag_id": [2, 3], "skip": 0, "limit": 3})
        assert response.status_code == 200
        assert response.json() == {"reviews": [{'id': 2, 'is_tagged': True, 'text': 'Test Review2'}, {'id': 3, 'is_tagged': True, 'text': 'Test Review3'}]}
    
    def test_delete_non_existent_tag(self):
        response = client.delete("/tags/999")
        assert response.status_code == 404


