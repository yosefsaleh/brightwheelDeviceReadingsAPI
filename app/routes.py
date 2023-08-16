from flask import request, jsonify
from app import app
from app.database import in_memory_db

@app.route('/store_readings', methods=['POST'])
def store_readings():
    data = request.get_json()

    device_id = data.get("id")
    readings = data.get("readings")

    if not device_id or not readings:
        return jsonify({"error": "Invalid data provided"}), 400

    if device_id not in in_memory_db:
        in_memory_db[device_id] = {}

    for reading in readings:
        timestamp = reading.get("timestamp")
        count = reading.get("count")

        if not timestamp or count is None:
            return jsonify({"error": "Malformed reading provided"}), 400

        # If the reading for this timestamp already exists, ignore it.
        if timestamp not in in_memory_db[device_id]:
            in_memory_db[device_id][timestamp] = count

    return jsonify({"message": "Readings stored successfully"}), 200


@app.route('/fetch_readings/<device_id>', methods=['GET'])
def fetch_readings(device_id):
    readings = in_memory_db.get(device_id, {})

    return jsonify({"readings": [{"timestamp": k, "count": v} for k, v in readings.items()]}), 200
