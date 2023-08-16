import unittest
from app import app
from app.database import in_memory_db

class TestRoutes(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_store_readings(self):
        data = {
            "id": "36d5658a-6908-479e-887e-a949ec199272",
            "readings": [{"timestamp": "2021-08-14T12:08:15+01:00", "count": 10}]
        }
        response = self.app.post('/store_readings', json=data)
        self.assertEqual(response.status_code, 200)

    def test_fetch_readings(self):
        device_id = "36d5658a-6908-479e-887e-a949ec199272"
        response = self.app.get(f'/fetch_readings/{device_id}')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        in_memory_db.clear()

if __name__ == "__main__":
    unittest.main()
