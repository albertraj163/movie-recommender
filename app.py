"""Flask web application for the movie recommendation system."""

from flask import Flask, jsonify, render_template, request

from recommender import MovieRecommender

app = Flask(__name__)
engine = MovieRecommender()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/stats")
def stats():
    return jsonify(engine.get_stats())


@app.route("/api/users")
def users():
    return jsonify(engine.get_users())


@app.route("/api/users/<int:user_id>/ratings")
def user_ratings(user_id: int):
    try:
        return jsonify(engine.get_user_ratings(user_id))
    except Exception as exc:
        return jsonify({"error": str(exc)}), 404


@app.route("/api/recommend/<int:user_id>")
def recommend(user_id: int):
    top_n = request.args.get("top_n", default=5, type=int)
    top_n = max(1, min(top_n, 10))
    try:
        return jsonify(
            {
                "user_id": user_id,
                "recommendations": engine.recommend_for_user(user_id, top_n),
            }
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5050))
    print(f"\n  CineMatch running at http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=True)
