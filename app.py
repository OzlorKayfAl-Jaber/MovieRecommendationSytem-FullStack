from flask import Flask, jsonify, request
from recommender import load_movies, MovieRecommender

app = Flask(__name__)

movies = load_movies("movies.csv")
recommender = MovieRecommender(movies)

@app.get("/health")
def health():
    return jsonify({"status": "ok", "movies": len(movies)})

@app.get("/recommend")
def recommend():
    title = request.args.get("title")
    if not title:
        return jsonify({"error": "Missing title"}), 400

    try:
        results = recommender.recommend(title)
    except ValueError:
        return jsonify({"error": "Movie not found"}), 404

    return jsonify({
        "query": title,
        "results": [
            {"title": m.title, "rating": m.rating, "score": round(s, 4)}
            for m, s in results
        ]
    })

if __name__ == "__main__":
    app.run(port=8000, debug=True)
