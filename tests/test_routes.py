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

        # Store some readings first
        self.app.post('/store_readings', json={
            "id": device_id,
            "readings": [{"timestamp": "2021-08-14T12:08:15+01:00", "count": 10}]
        })

        response = self.app.get(f'/fetch_readings/{device_id}')
        self.assertEqual(response.status_code, 200)

    def test_fetch_nonexistent_device(self):
        non_existent_device_id = "some-random-id"
        response = self.app.get(f'/fetch_readings/{non_existent_device_id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], "Device ID not found")

    def test_fetch_sorted_readings(self):
        # Storing out-of-order readings
        data = {
            "id": "test-device-id",
            "readings": [
                {"timestamp": "2021-08-15T12:10:15+01:00", "count": 30},
                {"timestamp": "2021-08-15T12:08:15+01:00", "count": 10},
                {"timestamp": "2021-08-15T12:09:15+01:00", "count": 20}
            ]
        }
        self.app.post('/store_readings', json=data)

        response = self.app.get('/fetch_readings/test-device-id')
        response_data = response.get_json()

        # The expected sorted order is 10, 20, 30 based on timestamps
        counts = [reading['count'] for reading in response_data['readings']]
        self.assertEqual(counts, [10, 20, 30])

    def tearDown(self):
        in_memory_db.clear()

if __name__ == "__main__":
    unittest.main()
