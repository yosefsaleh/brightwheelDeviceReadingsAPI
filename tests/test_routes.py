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

    def test_store_readings_with_missing_data(self):
        # Sending request with missing "count" data
        data = {
            "id": "36d5658a-6908-479e-887e-a949ec199272",
            "readings": [{"timestamp": "2021-08-14T12:08:15+01:00"}]
        }
        response = self.app.post('/store_readings', json=data)
        self.assertEqual(response.status_code, 400)

        # Verify the malformed reading isn't stored in our database
        readings = in_memory_db.get("36d5658a-6908-479e-887e-a949ec199272", {})
        self.assertNotIn("2021-08-14T12:08:15+01:00", readings)

    def test_malformed_json(self):
        response = self.app.post('/store_readings', data="this is not json")
        self.assertEqual(response.status_code, 415)  # Expect a bad request response

    def test_missing_fields(self):
        data = {"id": "36d5658a-6908-479e-887e-a949ec199272"}  # missing "readings" field
        response = self.app.post('/store_readings', json=data)
        self.assertEqual(response.status_code, 400)

    def test_invalid_data_types(self):
        data = {
            "id": "36d5658a-6908-479e-887e-a949ec199272",
            "readings": [{"timestamp": "2021-08-14T12:08:15+01:00", "count": "invalid_type"}]
        }
        response = self.app.post('/store_readings', json=data)
        self.assertEqual(response.status_code, 400)

    def test_fetch_readings(self):
        device_id = "36d5658a-6908-479e-887e-a949ec199272"
        response = self.app.get(f'/fetch_readings/{device_id}')
        self.assertEqual(response.status_code, 200)

    def test_fetch_nonexistent_device(self):
        non_existent_device_id = "some-random-id"
        response = self.app.get(f'/fetch_readings/{non_existent_device_id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['readings'], [])

    def test_fetch_without_data(self):
        device_id = "36d5658a-6908-479e-887e-a949ec199272"
        # Clear database to ensure it doesn't contain data for the given device_id
        in_memory_db.clear()
        response = self.app.get(f'/fetch_readings/{device_id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['readings'], [])

    def tearDown(self):
        in_memory_db.clear()

if __name__ == "__main__":
    unittest.main()
