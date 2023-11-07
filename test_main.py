from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_tag():
    tag_data = {
        "name": "TestTag"
    }
    response = client.post("/tags", json=tag_data)
    assert response.status_code == 201
    assert "id" in response.json()  # Check if the response contains the "id" field
    assert response.json()["name"] == "TestTag"

def test_get_reviews_with_tags():
    response = client.get("/reviews")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Check if the response is a list of reviews (modify as needed)

def test_add_tag_to_review():
    review_id = 1
    tag_ids = [1]
    response = client.post(f"/reviews/{review_id}/tags", json=tag_ids)
    assert response.status_code == 200
    assert "id" in response.json()  # Check if the response contains the "id" field (modify as needed)

def test_delete_tag():
    test_create_tag()
    tag_id = 1
    response = client.delete(f"/tags/{tag_id}")
    assert response.status_code == 200
    assert "message" in response.json()  # Check if the response contains a message (modify as needed)
