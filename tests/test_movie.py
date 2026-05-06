import pytest
from modules.movie import Movie


def make_movie(**kwargs):
    defaults = dict(
        movie_id=1,
        title="Test Movie (2010)",
        genres="Action|Drama",
        avg_rating=7.5,
    )
    defaults.update(kwargs)
    return Movie(**defaults)


class TestMovieInit:
    def test_title_stored(self):
        m = make_movie(title="Inception (2010)")
        assert m.title == "Inception"

    def test_title_stripped_of_year_parens(self):
        m = make_movie(title="Test Movie (2010)")
        assert m.title == "Test Movie"

    def test_year_extracted_from_title(self):
        m = make_movie(title="Test Movie (2010)")
        assert m.year == 2010

    def test_year_is_int(self):
        m = make_movie(title="Test Movie (1994)")
        assert isinstance(m.year, int)
        assert m.year == 1994

    def test_genre_split_multiple(self):
        m = make_movie(genres="Action|Drama|Thriller")
        assert m.genre == ["Action", "Drama", "Thriller"]

    def test_genre_single(self):
        m = make_movie(genres="Drama")
        assert m.genre == ["Drama"]

    def test_genre_no_genres_listed(self):
        m = make_movie(genres="(no genres listed)")
        assert m.genre == []

    def test_rating_is_float(self):
        m = make_movie(avg_rating="8.5")
        assert isinstance(m.rating, float)
        assert m.rating == 8.5

    def test_rating_numeric_input(self):
        m = make_movie(avg_rating=9.0)
        assert m.rating == 9.0


class TestMovieStr:
    def test_str_contains_title(self):
        m = make_movie(title="Inception (2010)")
        assert "Inception" in str(m)

    def test_str_contains_genres(self):
        m = make_movie(genres="Action|Sci-Fi")
        result = str(m)
        assert "Action" in result
        assert "Sci-Fi" in result

    def test_str_contains_year(self):
        m = make_movie(title="Test Movie (2010)")
        assert "2010" in str(m)

    def test_str_contains_rating(self):
        m = make_movie(avg_rating=8.8)
        assert "8.8" in str(m)


class TestMovieEq:
    def test_equal_identical_movies(self):
        m1 = make_movie()
        m2 = make_movie()
        assert m1 == m2

    def test_not_equal_different_title(self):
        m1 = make_movie(title="Movie A (2010)")
        m2 = make_movie(title="Movie B (2010)")
        assert m1 != m2

    def test_not_equal_different_rating(self):
        m1 = make_movie(avg_rating=8.0)
        m2 = make_movie(avg_rating=9.0)
        assert m1 != m2

    def test_not_equal_different_genre(self):
        m1 = make_movie(genres="Action")
        m2 = make_movie(genres="Drama")
        assert m1 != m2

    def test_not_equal_different_year(self):
        m1 = make_movie(title="Test Movie (1990)")
        m2 = make_movie(title="Test Movie (2000)")
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
        m1 = make_movie(title="Same Title (2000)", avg_rating=8.0)
        m2 = make_movie(title="Same Title (2010)", avg_rating=9.0)
        assert hash(m1) == hash(m2)

    def test_different_title_different_hash(self):
        m1 = make_movie(title="Movie A (2010)")
        m2 = make_movie(title="Movie B (2010)")
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
        m = make_movie(title="Test Movie (2010)")
        assert m.decade == "2010s"

    def test_decade_2019(self):
        m = make_movie(title="Test Movie (2019)")
        assert m.decade == "2010s"

    def test_decade_1994(self):
        m = make_movie(title="Test Movie (1994)")
        assert m.decade == "1990s"

    def test_decade_1975(self):
        m = make_movie(title="Test Movie (1975)")
        assert m.decade == "1970s"

    def test_is_classic_pre_1980(self):
        m = make_movie(title="Test Movie (1975)")
        assert m.is_classic is True

    def test_is_classic_1979(self):
        m = make_movie(title="Test Movie (1979)")
        assert m.is_classic is True

    def test_is_classic_1980_false(self):
        m = make_movie(title="Test Movie (1980)")
        assert m.is_classic is False

    def test_is_classic_modern_false(self):
        m = make_movie(title="Test Movie (2010)")
        assert m.is_classic is False

    def test_unknown_attribute_raises(self):
        m = make_movie()
        with pytest.raises(AttributeError):
            _ = m.nonexistent_attribute


class TestMovieLen:
    def test_len_multiple_genres(self):
        m = make_movie(genres="Action|Drama|Comedy")
        assert len(m) == 3

    def test_len_single_genre(self):
        m = make_movie(genres="Drama")
        assert len(m) == 1

    def test_len_no_genres(self):
        m = make_movie(genres="(no genres listed)")
        assert len(m) == 0

    def test_len_returns_int(self):
        m = make_movie(genres="Action|Drama")
        assert isinstance(len(m), int)
