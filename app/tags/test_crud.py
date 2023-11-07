from app.core.test_app import TestApp

OBJECT_ID = 0

class TestTag(TestApp):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.module = 'tags'

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
