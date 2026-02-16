import requests, os
from flask import Flask, jsonify, request

app = Flask(__name__)

EXPECTED_KEY = os.getenv("API_KEY")
APP_ENV = os.getenv("APP_ENV", "dev")


@app.route('/')
@app.route('/holidays')
def home():
    client_key = request.headers.get("X-API-KEY")
    if client_key != EXPECTED_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    url = "https://www.hebcal.com/hebcal?v=1&cfg=json&maj=on&year=now"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        holidays = [{"name": i.get("title"), "date": i.get("date")} for i in data.get("items", [])]

        return jsonify({
            "environment": APP_ENV,
            "status": "Secure Access Granted",
            "holidays": holidays
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)