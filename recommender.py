from __future__ import annotations
import csv
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Sequence

TOKEN_SPLIT_PATTERN = re.compile(r"[,\|;/]")

@dataclass(frozen=True)
class Movie:
    movie_id: str
    title: str
    genres: Tuple[str, ...]
    keywords: Tuple[str, ...]
    rating: float

def _normalize_token(token: str) -> str:
    return token.strip().lower().replace(" ", "_")

def _split_tokens(raw: str) -> List[str]:
    if not raw:
        return []
    parts = TOKEN_SPLIT_PATTERN.split(raw)
    return [_normalize_token(p) for p in parts if p]

def _parse_float(raw: str, default: float = 0.0) -> float:
    try:
        return float(raw)
    except:
        return default

def load_movies(csv_path: str) -> List[Movie]:
    path = Path(csv_path)
    movies = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row["title"]
            movie_id = row.get("id", title)
            genres = tuple(_split_tokens(row.get("genres", "")))
            keywords = tuple(_split_tokens(row.get("keywords", "")))
            rating = _parse_float(row.get("rating", 0))
            movies.append(Movie(movie_id, title, genres, keywords, rating))
    return movies

class MovieRecommender:
    def __init__(self, movies: Sequence[Movie]):
        self.movies = list(movies)
        self._index = {m.title.lower(): i for i, m in enumerate(self.movies)}
        self._vectors = [self._vectorize(m) for m in self.movies]
        self._norms = [self._norm(v) for v in self._vectors]

    def _vectorize(self, movie: Movie) -> Dict[str, float]:
        vec = Counter()
        for g in movie.genres:
            vec[f"g:{g}"] += 2.0
        for k in movie.keywords:
            vec[f"k:{k}"] += 1.0
        vec["rating"] = movie.rating / 10
        return dict(vec)

    def _dot(self, a, b):
        return sum(v * b.get(k, 0) for k, v in a.items())

    def _norm(self, vec):
        return math.sqrt(sum(v*v for v in vec.values()))

    def recommend(self, title: str, top_k=5):
        idx = self._index.get(title.lower())
        if idx is None:
            raise ValueError("Movie not found")

        target_vec = self._vectors[idx]
        target_norm = self._norms[idx]

        scores = []
        for i, movie in enumerate(self.movies):
            if i == idx:
                continue
            score = self._dot(target_vec, self._vectors[i]) / (target_norm * self._norms[i])
            scores.append((movie, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
