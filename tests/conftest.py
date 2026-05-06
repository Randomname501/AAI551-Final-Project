import matplotlib
matplotlib.use('Agg')

import pytest
import pandas as pd
from modules.movie import Movie
from modules.recommender import Recommender

MOVIE_COLUMNS = ["movieId", "title", "genres"]
RATING_COLUMNS = ["userId", "movieId", "rating", "timestamp"]

MOVIE_ROWS = [
    (1, "Movie A (2010)", "Action|Drama"),
    (2, "Movie B (1975)", "Drama|Comedy"),
    (3, "Movie C (1985)", "Action|Thriller"),
    (4, "Movie D (1960)", "Comedy|Romance"),
    (5, "Movie E (2000)", "Action|Comedy"),
]

# One rating per movie so avg_rating == that value: 8.5, 7.0, 9.0, 6.5, 8.0
RATING_ROWS = [
    (1, 1, 8.5, 0),
    (1, 2, 7.0, 0),
    (1, 3, 9.0, 0),
    (1, 4, 6.5, 0),
    (1, 5, 8.0, 0),
]

# https://docs.pytest.org/en/stable/explanation/fixtures.html
@pytest.fixture
def sample_movie():
    return Movie(1, "Movie A (2010)", "Action|Drama", 8.5)


@pytest.fixture
def classic_movie():
    return Movie(2, "Movie B (1975)", "Drama|Comedy", 7.0)


@pytest.fixture
def sample_csv_paths(tmp_path):
    movies_path = tmp_path / "movies.csv"
    ratings_path = tmp_path / "ratings.csv"
    pd.DataFrame(MOVIE_ROWS, columns=MOVIE_COLUMNS).to_csv(movies_path, index=False)
    pd.DataFrame(RATING_ROWS, columns=RATING_COLUMNS).to_csv(ratings_path, index=False)
    return str(movies_path), str(ratings_path)


@pytest.fixture
def recommender(sample_csv_paths):
    movies_path, ratings_path = sample_csv_paths
    return Recommender(movies_path, ratings_path)
