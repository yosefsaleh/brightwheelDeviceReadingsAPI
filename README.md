# Brightwheel Device Readings API

## Project Summary

This project provides a RESTful API to store and fetch device readings. It has been designed to handle various edge cases and to provide meaningful error messages where necessary. The core functionality revolves around the two main endpoints: one for storing readings and another for fetching readings based on device ID.

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
**Note When Running**:

Open a new terminal window to run any curl commands. Should not try to run in the same window that we started the Flask server in.

## Reflection

**What roadblocks did you run into when writing your code (i.e., where did you spend the bulk of your time)?**

While the initial implementation of the API was relatively straightforward, I dedicated a significant portion of my time to identifying and handling edge cases. I wanted to ensure the robustness and reliability of the solution, so I tried to anticipate possible issues and anomalies that could arise during real-world usage. As a result, a good portion of my time was spent crafting various test cases and trying to "break" the API in different, unexpected ways. I consistently ran into challenges when determining how the API should handle incomplete or malformed data, especially as I dug deeper into the myriad ways data could be mishandled or misinterpreted. Making sure that the system gracefully handles these edge cases while providing meaningful feedback to the user was one of the primary roadblocks I encountered.

**If you had more time, what part of your project would you refactor? What other tradeoffs did you make?**

Given more time, I would consider refactoring the way data validation is handled. While the current system is robust, there might be opportunities to make it more modular or efficient. For instance, I could integrate a dedicated data validation library or framework that provides more comprehensive and maintainable validation mechanisms.

Regarding the in-memory storage approach, it was a requirement for this assignment, and I adhered to it. While it's efficient for quick access and keeps the solution simple, it's worth noting that in a more extended real-world application, we might want to consider persistent storage solutions, like a database, for longevity and more advanced querying capabilities. The tradeoff made here was in adhering to the assignment's requirements while ensuring optimal functionality within those constraints. Another tradeoff I made was prioritizing functionality and robustness over optimizations. Some operations, like sorting readings by timestamps, could potentially be optimized further by considering specific data structures or algorithms.
