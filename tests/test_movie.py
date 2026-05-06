import pytest
from modules.movie import Movie


def make_movie(**kwargs):
    defaults = dict(
        imdb_title_id="tt0000001",
        original_title="Test Movie",
        year=2010,
        genre="Action, Drama",
        duration=120,
        director="Test Director",
        writer="Test Writer",
        production_company="Test Studio",
        actors="Actor One, Actor Two",
        description="A test description",
        avg_vote=7.5,
        votes=1000,
    )
    defaults.update(kwargs)
    return Movie(**defaults)


class TestMovieInit:
    def test_title_stored(self):
        m = make_movie(original_title="Inception")
        assert m.title == "Inception"

    def test_genre_split_multiple(self):
        m = make_movie(genre="Action, Drama, Thriller")
        assert m.genre == ["Action", "Drama", "Thriller"]

    def test_genre_single(self):
        m = make_movie(genre="Drama")
        assert m.genre == ["Drama"]

    def test_rating_is_float(self):
        m = make_movie(avg_vote="8.5")
        assert isinstance(m.rating, float)
        assert m.rating == 8.5

    def test_rating_numeric_input(self):
        m = make_movie(avg_vote=9.0)
        assert m.rating == 9.0

    def test_year_is_int(self):
        m = make_movie(year="2010")
        assert isinstance(m.year, int)
        assert m.year == 2010

    def test_director_stored(self):
        m = make_movie(director="Christopher Nolan")
        assert m.director == "Christopher Nolan"

    def test_actors_split_multiple(self):
        m = make_movie(actors="Actor One, Actor Two, Actor Three")
        assert m.actors == ["Actor One", "Actor Two", "Actor Three"]

    def test_actors_single(self):
        m = make_movie(actors="Solo Actor")
        assert m.actors == ["Solo Actor"]


class TestMovieStr:
    def test_str_contains_title(self):
        m = make_movie(original_title="Inception")
        assert "Inception" in str(m)

    def test_str_contains_genres(self):
        m = make_movie(genre="Action, Sci-Fi")
        result = str(m)
        assert "Action" in result
        assert "Sci-Fi" in result

    def test_str_contains_director(self):
        m = make_movie(director="Christopher Nolan")
        assert "Christopher Nolan" in str(m)

    def test_str_contains_rating(self):
        m = make_movie(avg_vote=8.8)
        assert "8.8" in str(m)


class TestMovieEq:
    def test_equal_identical_movies(self):
        m1 = make_movie()
        m2 = make_movie()
        assert m1 == m2

    def test_not_equal_different_title(self):
        m1 = make_movie(original_title="Movie A")
        m2 = make_movie(original_title="Movie B")
        assert m1 != m2

    def test_not_equal_different_rating(self):
        m1 = make_movie(avg_vote=8.0)
        m2 = make_movie(avg_vote=9.0)
        assert m1 != m2

    def test_not_equal_different_director(self):
        m1 = make_movie(director="Director A")
        m2 = make_movie(director="Director B")
        assert m1 != m2

    def test_not_equal_different_genre(self):
        m1 = make_movie(genre="Action")
        m2 = make_movie(genre="Drama")
        assert m1 != m2

    def test_not_equal_to_string(self):
        m = make_movie()
        assert m != "not a movie"

    def test_not_equal_to_int(self):
        m = make_movie()
        assert m != 42

    def test_not_equal_to_none(self):
        m = make_movie()
        assert m != None


class TestMovieHash:
    def test_hash_returns_int(self):
        m = make_movie()
        assert isinstance(hash(m), int)

    def test_same_title_same_hash(self):
        m1 = make_movie(original_title="Same Title", avg_vote=8.0)
        m2 = make_movie(original_title="Same Title", avg_vote=9.0)
        assert hash(m1) == hash(m2)

    def test_different_title_different_hash(self):
        m1 = make_movie(original_title="Movie A")
        m2 = make_movie(original_title="Movie B")
        assert hash(m1) != hash(m2)

    def test_equal_movies_deduplicate_in_set(self):
        m1 = make_movie()
        m2 = make_movie()
        assert len({m1, m2}) == 1

    def test_usable_as_dict_key(self):
        m = make_movie()
        d = {m: "value"}
        assert d[m] == "value"

    def test_usable_in_set(self):
        m = make_movie()
        s = {m}
        assert m in s


class TestMovieGetattr:
    def test_decade_2010(self):
        m = make_movie(year=2010)
        assert m.decade == "2010s"

    def test_decade_2019(self):
        m = make_movie(year=2019)
        assert m.decade == "2010s"

    def test_decade_1994(self):
        m = make_movie(year=1994)
        assert m.decade == "1990s"

    def test_decade_1975(self):
        m = make_movie(year=1975)
        assert m.decade == "1970s"

    def test_is_classic_pre_1980(self):
        m = make_movie(year=1975)
        assert m.is_classic is True

    def test_is_classic_1979(self):
        m = make_movie(year=1979)
        assert m.is_classic is True

    def test_is_classic_1980_false(self):
        m = make_movie(year=1980)
        assert m.is_classic is False

    def test_is_classic_modern_false(self):
        m = make_movie(year=2010)
        assert m.is_classic is False

    def test_unknown_attribute_raises(self):
        m = make_movie()
        with pytest.raises(AttributeError):
            _ = m.nonexistent_attribute
