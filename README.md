# Brightwheel Device Readings API

## Project Summary

This project provides a simple Flask web API to store and fetch device readings. The data is temporarily stored in an in-memory database.

## Startup Instructions

### Prerequisites

1. Ensure you have Python version 3.8.9 installed. You can check your Python version with the command:
```bash
python --version
```

2. Install Flask:
```bash
pip install Flask
```

### Running the Web API

1. Navigate to the project directory:
```bash
cd path/to/brightwheelDeviceReadingsAPI
```

2. Run the application:
```bash
python run.py
```

**Note**: If you have PyCharm installed, you can also open the project in PyCharm and simply click the "Run" button on `run.py`.

## Running the Tests

From the project directory, run:
```bash
python -m unittest tests/test_routes.py
```

## API Documentation

### Storing Readings

- **Endpoint**: `/store_readings`
- **Method**: `POST`
- **Headers**:
  - `Content-Type: application/json`
- **Body**:
```json
{
  "id": "device_id_string",
  "readings": [
      {
          "timestamp": "timestamp_string",
          "count": 10
      },
      ...
  ]
}
```

**Sample Curl Command**:
```bash
curl -X POST http://127.0.0.1:5000/store_readings -H "Content-Type: application/json" -d '{"id": "device_1", "readings": [{"timestamp": "2021-08-14T12:08:15+01:00", "count": 10}]}'
```

### Fetching Readings

- **Endpoint**: `/fetch_readings/<device_id>`
- **Method**: `GET`

**Sample Curl Command**:
```bash
curl http://127.0.0.1:5000/fetch_readings/device_1
```

## Reflection

When implementing the solution, the majority of time was spent on identifying and handling edge cases and writing robust test cases to ensure the reliability of the API. The aim was to challenge the API in different ways and ensure its resilience.

Should there have been more time, one would contemplate the idea of implementing more comprehensive logging for better traceability and error diagnosis. Additionally, integrating a persistent database or caching mechanism for scalability would be considered.

While the current architecture using an in-memory storage serves the immediate requirement, it’s worth noting that this is not suitable for production as data would be lost when the server restarts. Future enhancements would benefit from integrating a persistent storage system.
