# TODO Please complete the test case here
# TODO Please complete the test case here
import json

import pytest
from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app

# Create a TestClient for the app
client = TestClient(app)

# Write test functions
def test_read_reviews():
    response = client.get("/reviews")
    assert response.status_code == 200
    assert response.json() == [
  {
    "review": {
      "text": "Nice Post",
      "is_tagged": True,
      "id": 1
    },
    "tags": []
  },
  {
    "review": {
      "text": "This is a test review",
      "is_tagged": False,
      "id": 2
    },
    "tags": []
  },
  {
    "review": {
      "text": "This is a test review",
      "is_tagged": False,
      "id": 3
    },
    "tags": []
  },
  {
    "review": {
      "text": "This is a test review",
      "is_tagged": False,
      "id": 4
    },
    "tags": []
  },
  {
    "review": {
      "text": "This is a test review",
      "is_tagged": False,
      "id": 5
    },
    "tags": []
  },
  {
    "review": {
      "text": "This is a test review",
      "is_tagged": False,
      "id": 6
    },
    "tags": []
  },
  {
    "review": {
      "text": "This is a test review",
      "is_tagged": False,
      "id": 7
    },
    "tags": []
  },
  {
    "review": {
      "text": "This is a test review",
      "is_tagged": False,
      "id": 8
    },
    "tags": []
  }
]

def test_create_review():
    review_data = {"text": "This is a test review", "is_tagged": False}
    response = client.post("/create-review", json=review_data)
    assert response.status_code == 200

def test_create_tag():
    tag_data = {"name": "Test Tag"}
    response = client.post("/tags", json=tag_data)
    assert response.status_code == 200

def test_add_tags_to_review():
    # Test data
    review_id = 1  # Replace with the valid review ID
    data = {"tags": ["tag1", "tag2"]}
    # Make a POST request to your API route
    response = client.post(f"/reviews/{review_id}/tags", json=data["tags"])
    print(response)

    # Check the response status code
    assert response.status_code == 200

    # Check the response content
    data = response.json()
    assert data["message"] == "Tags added successfully"



def test_delete_tag():
    tag_data = {"name": "Test Tag"}
    response = client.post("/tags", json=tag_data)
    tag_id = response.json()["id"]

    response = client.delete(f"/tags/{tag_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Tag deleted successfully"}

if __name__ == "__main__":
    pytest.main()
