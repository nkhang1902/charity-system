from flask import Flask, request, jsonify
import joblib
from lightfm import LightFM
import numpy as np

app = Flask(__name__)

model = joblib.load("lightfm_model.pkl")

@app.route("/recommend", methods=["POST"])
def recommend():
    """
    Example request:
    {
        "user_id": 5,
        "item_ids": [1, 2, 3, 4]
    }
    """
    try:
        data = request.get_json()
        user_id = data["user_id"]
        item_ids = np.array(data["item_ids"])

        scores = model.predict(user_id, item_ids)

        top_indices = np.argsort(-scores)
        top_items = item_ids[top_indices].tolist()

        return jsonify({
            "user_id": user_id,
            "recommendations": top_items
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
