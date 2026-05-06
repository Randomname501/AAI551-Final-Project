import pytest
import pandas as pd
from modules.movie import Movie
from modules.recommender import Recommender

COLUMNS = [
    "imdb_title_id", "original_title", "year", "genre", "duration",
    "director", "writer", "production_company", "actors", "description",
    "avg_vote", "votes",
]

SAMPLE_ROWS = [
    ("tt0000001", "Movie A", 2010, "Action, Drama",   120, "Director X", "Writer A", "Studio A", "Actor One, Actor Two",    "Desc A", 8.5, 10000),
    ("tt0000002", "Movie B", 1975, "Drama, Comedy",    90, "Director Y", "Writer B", "Studio B", "Actor Two, Actor Three",  "Desc B", 7.0,  5000),
    ("tt0000003", "Movie C", 1985, "Action, Thriller", 100, "Director X", "Writer C", "Studio C", "Actor One, Actor Four",  "Desc C", 9.0, 20000),
    ("tt0000004", "Movie D", 1960, "Comedy, Romance",   80, "Director Z", "Writer D", "Studio D", "Actor Five",             "Desc D", 6.5,  3000),
    ("tt0000005", "Movie E", 2000, "Action, Comedy",   110, "Director Y", "Writer E", "Studio E", "Actor Three, Actor Five","Desc E", 8.0, 15000),
]


@pytest.fixture
def sample_movie():
    row = SAMPLE_ROWS[0]
    return Movie(*row)


@pytest.fixture
def classic_movie():
    row = SAMPLE_ROWS[1]
    return Movie(*row)


@pytest.fixture
def sample_csv(tmp_path):
    df = pd.DataFrame(SAMPLE_ROWS, columns=COLUMNS)
    csv_path = tmp_path / "test_movies.csv"
    df.to_csv(csv_path, index=False)
    return str(csv_path)


@pytest.fixture
def recommender(sample_csv):
    return Recommender(sample_csv)
