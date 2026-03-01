"""
SHL Assessment Recommendation API
Flask-based REST API with health check and recommendation endpoints.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recommender import SHLRecommender

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates")
app = Flask(__name__, template_folder=TEMPLATE_DIR)
CORS(app)  # Enable CORS for frontend

# Global recommender instance
recommender = None

def get_recommender():
    global recommender
    if recommender is None:
        data_path = os.environ.get("ASSESSMENT_DATA_PATH", 
                                   os.path.join(os.path.dirname(__file__), "..", "data", "shl_assessments.json"))
        recommender = SHLRecommender(data_path=data_path)
        recommender.load()
    return recommender


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    try:
        rec = get_recommender()
        return jsonify({
            "status": "healthy",
            "num_assessments": len(rec.assessments),
            "model": "TF-IDF + Keyword Boosting",
            "version": "1.0.0"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500


@app.route("/recommend", methods=["POST"])
def recommend():
    """
    Assessment recommendation endpoint.
    
    Request body:
    {
        "query": "string - natural language query or job description"
    }
    
    Response:
    {
        "recommended_assessments": [
            {
                "assessment_name": "string",
                "url": "string",
                "test_types": ["K", "P", ...],
                "duration": "string",
                "remote_testing": bool,
                "adaptive_irt_support": bool,
                "description": "string",
                "relevance_score": float
            }
        ]
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400
        
        query = data.get("query", "").strip()
        
        if not query:
            return jsonify({"error": "Query field is required"}), 400
        
        if len(query) < 3:
            return jsonify({"error": "Query is too short"}), 400
        
        top_k = min(int(data.get("top_k", 10)), 10)  # Max 10
        top_k = max(top_k, 1)  # Min 1
        
        rec = get_recommender()
        recommendations = rec.recommend(query, top_k=top_k)
        formatted = rec.format_recommendations(recommendations)
        
        return jsonify({
            "recommended_assessments": formatted,
            "query": query,
            "num_results": len(formatted)
        }), 200
    
    except FileNotFoundError as e:
        return jsonify({"error": f"Assessment data not loaded: {str(e)}"}), 503
    except Exception as e:
        return jsonify({"error": f"Recommendation failed: {str(e)}"}), 500


@app.route("/app", methods=["GET"])
def frontend():
    """Serve the frontend web app."""
    return send_from_directory(TEMPLATE_DIR, "index.html")


@app.route("/", methods=["GET"])
def root():
    """Root endpoint with API info."""
    return jsonify({
        "name": "SHL Assessment Recommendation API",
        "version": "1.0.0",
        "endpoints": {
            "GET /health": "Health check",
            "POST /recommend": "Get assessment recommendations",
        },
        "usage": {
            "url": "/recommend",
            "method": "POST",
            "body": {"query": "Your job description or query here"},
            "example": {
                "query": "I am hiring Java developers who can collaborate with business teams"
            }
        }
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "false").lower() == "true"
    
    print(f"Starting SHL Recommendation API on port {port}")
    print("Pre-loading recommender...")
    
    try:
        get_recommender()
        print("Recommender loaded successfully!")
    except Exception as e:
        print(f"Warning: Could not pre-load recommender: {e}")
        print("It will be loaded on first request.")
    
    app.run(host="0.0.0.0", port=port, debug=debug)
