"""
SHL Assessment Recommendation API
"""
from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recommender import SHLRecommender

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates")
app = Flask(__name__, template_folder=TEMPLATE_DIR)
CORS(app)

recommender = None

def get_recommender():
    global recommender
    if recommender is None:
        data_path = os.environ.get(
            "ASSESSMENT_DATA_PATH",
            os.path.join(os.path.dirname(__file__), "..", "data", "shl_assessments.json")
        )
        recommender = SHLRecommender(data_path=data_path)
        recommender.load()
    return recommender


@app.route("/health", methods=["GET"])
def health_check():
    try:
        rec = get_recommender()
        return jsonify({
            "status": "healthy",
            "num_assessments": len(rec.assessments),
            "model": "TF-IDF + Keyword Boosting",
            "version": "1.0.0"
        }), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


@app.route("/recommend", methods=["GET"])
def recommend_get():
    return jsonify({
        "error": "Method Not Allowed",
        "message": "Use POST with a JSON body containing a 'query' field.",
        "example": {"query": "Java developer with collaboration skills"}
    }), 405


@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400
        query = data.get("query", "").strip()
        if not query:
            return jsonify({"error": "Query field is required"}), 400
        if len(query) < 3:
            return jsonify({"error": "Query is too short"}), 400
        top_k = max(1, min(int(data.get("top_k", 10)), 10))
        rec = get_recommender()
        recommendations = rec.recommend(query, top_k=top_k)
        formatted = rec.format_recommendations(recommendations)
        return jsonify({
            "recommended_assessments": formatted,
            "query": query,
            "num_results": len(formatted)
        }), 200
    except FileNotFoundError as e:
        return jsonify({"error": "Assessment data not loaded: " + str(e)}), 503
    except Exception as e:
        return jsonify({"error": "Recommendation failed: " + str(e)}), 500


@app.route("/app", methods=["GET"])
def frontend():
    return send_from_directory(TEMPLATE_DIR, "index.html")


@app.route("/", methods=["GET"])
def root():
    return redirect("/app")


@app.route("/api", methods=["GET"])
def api_info():
    return jsonify({
        "name": "SHL Assessment Recommendation API",
        "version": "1.0.0",
        "endpoints": {
            "GET  /health": "Health check",
            "POST /recommend": "Get top-10 assessment recommendations",
            "GET  /app": "Web UI"
        },
        "usage": {
            "method": "POST",
            "url": "/recommend",
            "content_type": "application/json",
            "body": {"query": "your job description here"}
        }
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("Pre-loading recommender...")
    try:
        get_recommender()
        print("Recommender loaded successfully!")
    except Exception as e:
        print("Warning: Could not pre-load recommender:", e)
    app.run(host="0.0.0.0", port=port, debug=False)