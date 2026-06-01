"""User-based collaborative filtering movie recommender."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

DATA_DIR = Path(__file__).parent


class MovieRecommender:
    def __init__(
        self,
        ratings_path: str | Path = DATA_DIR / "sample_ratings.csv",
        movies_path: str | Path = DATA_DIR / "movies.csv",
    ):
        self.ratings = pd.read_csv(ratings_path)
        self.movies = pd.read_csv(movies_path)
        self._matrix = self._build_matrix()
        self._similarity = self._build_similarity()

    def _build_matrix(self) -> pd.DataFrame:
        return (
            self.ratings.pivot_table(
                index="userId", columns="movieId", values="rating"
            ).fillna(0)
        )

    def _build_similarity(self) -> pd.DataFrame:
        sim = cosine_similarity(self._matrix)
        return pd.DataFrame(
            sim, index=self._matrix.index, columns=self._matrix.index
        )

    def get_users(self) -> list[dict]:
        users = sorted(self.ratings["userId"].unique())
        stats = []
        for user_id in users:
            user_ratings = self.ratings[self.ratings["userId"] == user_id]
            stats.append(
                {
                    "id": int(user_id),
                    "rating_count": len(user_ratings),
                    "avg_rating": round(user_ratings["rating"].mean(), 2),
                }
            )
        return stats

    def get_user_ratings(self, user_id: int) -> list[dict]:
        user_ratings = self.ratings[self.ratings["userId"] == user_id]
        merged = user_ratings.merge(self.movies, on="movieId")
        merged = merged.sort_values("rating", ascending=False)
        return [
            {
                "movie_id": int(row.movieId),
                "title": row.title,
                "genre": row.genre,
                "year": int(row.year),
                "rating": float(row.rating),
            }
            for row in merged.itertuples()
        ]

    def recommend_for_user(self, user_id: int, top_n: int = 5) -> list[dict]:
        if user_id not in self._matrix.index:
            raise ValueError(f"User {user_id} not found.")

        watched = set(
            self.ratings[self.ratings["userId"] == user_id]["movieId"].tolist()
        )
        user_sim = (
            self._similarity[user_id].drop(user_id).sort_values(ascending=False)
        )

        scores: dict[int, float] = {}
        weights: dict[int, float] = {}

        for similar_user, similarity in user_sim.items():
            if similarity <= 0:
                continue
            for movie_id, rating in self._matrix.loc[similar_user].items():
                if movie_id in watched or rating <= 0:
                    continue
                scores[movie_id] = scores.get(movie_id, 0) + similarity * rating
                weights[movie_id] = weights.get(movie_id, 0) + similarity

        ranked = sorted(
            (
                (movie_id, scores[movie_id] / weights[movie_id])
                for movie_id in scores
            ),
            key=lambda item: item[1],
            reverse=True,
        )[:top_n]

        recommendations = []
        for movie_id, predicted_rating in ranked:
            movie = self.movies[self.movies["movieId"] == movie_id].iloc[0]
            recommendations.append(
                {
                    "movie_id": int(movie_id),
                    "title": movie.title,
                    "genre": movie.genre,
                    "year": int(movie.year),
                    "predicted_rating": round(predicted_rating, 2),
                }
            )
        return recommendations

    def get_stats(self) -> dict:
        return {
            "total_users": int(self.ratings["userId"].nunique()),
            "total_movies": int(self.movies.shape[0]),
            "total_ratings": int(len(self.ratings)),
            "avg_rating": round(float(self.ratings["rating"].mean()), 2),
        }


def main():
    engine = MovieRecommender()
    print("Dataset stats:", engine.get_stats())
    print("Recommendations for user 1:", engine.recommend_for_user(1))


if __name__ == "__main__":
    main()
