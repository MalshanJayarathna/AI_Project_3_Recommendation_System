# =============================================================================
# app.py — Flask Web Application
# Project : DecodeLabs AI Project 3 — AI Course Recommendation System
# Author  : DecodeLabs
# Version : 1.0.0
#
# Description:
#   This module serves as the backend web server for the AI Course
#   Recommendation System. It exposes three HTTP endpoints:
#
#       GET  /           → Serves the main HTML web page
#       POST /recommend  → Accepts user interests (JSON), returns top-5
#                          course recommendations with similarity scores
#       GET  /courses    → Returns all courses in the dataset as JSON
#
# How It Works:
#   1. On startup, the course dataset (data/items.csv) is loaded into memory.
#   2. A TF-IDF matrix is built once from all course descriptions.
#   3. Each POST to /recommend vectorises the user's query using the same
#      TF-IDF vocabulary, computes cosine similarity against every course
#      vector, sorts by score, and returns the top 5 matches as JSON.
#
# Usage:
#   python app.py          ← runs in development/debug mode on port 5000
#   Visit http://127.0.0.1:5000 in your browser
#
# NOTE: For production deployment, replace Flask's built-in server with
#       a WSGI server such as Gunicorn:
#           gunicorn -w 4 app:app
# =============================================================================

from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import sys

# ── Initialise Flask application ──────────────────────────────────────────────
app = Flask(__name__)

# ── Resolve dataset path relative to this file ────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "items.csv")

# ── Load dataset at startup (once, not on every request) ──────────────────────
if not os.path.exists(DATA_PATH):
    print(f"[ERROR] Dataset not found: {DATA_PATH}")
    sys.exit(1)

df = pd.read_csv(DATA_PATH)
df.dropna(subset=["description"], inplace=True)   # Remove rows with no description
df.reset_index(drop=True, inplace=True)

# ── Build TF-IDF matrix once at startup ───────────────────────────────────────
# TF-IDF converts each course description into a numerical vector.
# stop_words="english" removes common words like 'the', 'is', 'and'.
# ngram_range=(1, 2) captures both single words and two-word phrases.
vectorizer   = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1)
tfidf_matrix = vectorizer.fit_transform(df["description"])

print(f"[INFO] Loaded {len(df)} courses | TF-IDF matrix shape: {tfidf_matrix.shape}")


# ── Route 1: Home Page ────────────────────────────────────────────────────────
@app.route("/")
def index():
    """Render and serve the main web interface (templates/index.html)."""
    return render_template("index.html")


# ── Route 2: Recommendation API ───────────────────────────────────────────────
@app.route("/recommend", methods=["POST"])
def recommend():
    """
    Accept user interests via a POST request and return top-5 course
    recommendations ranked by cosine similarity.

    Request Body (JSON):
        { "interests": "python machine learning automation" }

    Response (JSON):
        {
            "query": "python machine learning automation",
            "recommendations": [
                {
                    "rank": 1,
                    "title": "Machine Learning Fundamentals",
                    "category": "Machine Learning",
                    "description": "...",
                    "similarity_score": 0.2748
                },
                ...
            ]
        }

    Error Response (JSON, HTTP 400):
        { "error": "Please enter your interests." }
    """
    # Parse incoming JSON body
    data       = request.get_json(silent=True) or {}
    user_input = data.get("interests", "").strip()

    # Validate — reject empty input
    if not user_input:
        return jsonify({"error": "Please enter your interests."}), 400

    # Step 1: Transform user's query into a TF-IDF vector using the
    #         same vocabulary that was fitted on the course descriptions.
    user_vector = vectorizer.transform([user_input])

    # Step 2: Compute cosine similarity between the user vector and
    #         every course vector in the matrix.
    #         Result shape: (1, n_courses) → flattened to (n_courses,)
    scores = cosine_similarity(user_vector, tfidf_matrix).flatten()

    # Step 3: Attach scores to the DataFrame and sort descending
    result_df                   = df.copy()
    result_df["similarity_score"] = scores
    top5 = (
        result_df
        .sort_values("similarity_score", ascending=False)
        .head(5)
        .reset_index(drop=True)
    )

    # Step 4: Build JSON-serialisable list of recommendations
    recommendations = [
        {
            "rank":             rank,
            "title":            row["title"],
            "category":         row["category"],
            "description":      row["description"],
            "similarity_score": round(float(row["similarity_score"]), 4),
        }
        for rank, (_, row) in enumerate(top5.iterrows(), start=1)
    ]

    return jsonify({"recommendations": recommendations, "query": user_input})


# ── Route 3: All Courses ───────────────────────────────────────────────────────
@app.route("/courses")
def all_courses():
    """
    Return the complete course catalogue as JSON.

    Response (JSON):
        {
            "total": 20,
            "courses": [
                { "title": "...", "category": "...", "description": "..." },
                ...
            ]
        }
    """
    courses = df[["title", "category", "description"]].to_dict(orient="records")
    return jsonify({"courses": courses, "total": len(courses)})


# ── Entry Point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # debug=True enables auto-reload and detailed error pages (development only).
    # Set debug=False and use a production WSGI server for live deployment.
    app.run(debug=True, host="127.0.0.1", port=5000)
