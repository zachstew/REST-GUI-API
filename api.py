# api.py - Flask API that receives purchase data from the Tkinter GUI
from decimal import Decimal, InvalidOperation

from flask import Flask, request, jsonify

app = Flask(__name__)

MAX_PRICE = Decimal("1000.00")

@app.route("/")
def home():
    return "Purchase API is running. POST JSON to /submit."

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Required text fields
    for field in ("product_id", "description", "name", "email"):
        if not str(data.get(field, "")).strip():
            return jsonify({"error": f"Missing {field}"}), 400

    # Same email rule as the GUI (the server should never trust the client)
    if "@" not in data["email"]:
        return jsonify({"error": "Invalid email address"}), 400

    # Price must be a number and <= $1,000.00
    try:
        price = Decimal(str(data.get("price")))
    except (InvalidOperation, TypeError):
        return jsonify({"error": "Price must be a number"}), 400
    if price < 0 or price > MAX_PRICE:
        return jsonify({"error": "Price must be between $0.00 and $1,000.00"}), 400

    print("Received purchase:", data)  # shows in the terminal running the API
    return jsonify({"status": "ok", "received": data}), 200


if __name__ == "__main__":
    app.run(port=5001, debug=True)