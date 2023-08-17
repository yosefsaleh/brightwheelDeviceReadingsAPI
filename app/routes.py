from flask import request, jsonify
from app import app
from app.database import in_memory_db

@app.route('/store_readings', methods=['POST'])
def store_readings():
    data = request.get_json()

    device_id = data.get("id")
    readings = data.get("readings")

    if not device_id:
        return jsonify({"error": "No id was provided"}), 400

    if not readings:
        return jsonify({"error": "No readings were provided"}), 400

    # Basic type validation
    if not isinstance(device_id, str):
        return jsonify({"error": "Invalid data type for device id"}), 400
    if not isinstance(readings, list):
        return jsonify({"error": "Invalid data type for readings"}), 400

    if device_id not in in_memory_db:
        in_memory_db[device_id] = {}

    for reading in readings:
        timestamp = reading.get("timestamp")
        count = reading.get("count")

        if not timestamp:
            return jsonify({"error": "Timestamp is missing in the reading"}), 400
        if count is None:
            return jsonify({"error": "Count is missing in the reading"}), 400

        # Check the types for the reading data
        if not isinstance(timestamp, str):
            return jsonify({"error": "Invalid data type for timestamp"}), 400
        if not isinstance(count, (int, float)):
            return jsonify({"error": "Invalid data type for count"}), 400

        # If the reading for this timestamp already exists, ignore it.
        if timestamp not in in_memory_db[device_id]:
            in_memory_db[device_id][timestamp] = count

    return jsonify({"message": "Readings stored successfully"}), 200

@app.route('/fetch_readings/<device_id>', methods=['GET'])
def fetch_readings(device_id):
    readings = in_memory_db.get(device_id, {})

    return jsonify({"readings": [{"timestamp": k, "count": v} for k, v in readings.items()]}), 200
