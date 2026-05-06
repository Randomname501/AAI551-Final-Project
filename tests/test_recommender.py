import pytest
from modules.movie import Movie


class TestLoadData:
    def test_movies_count(self, recommender):
        assert len(recommender.movies) == 5

    def test_movies_are_movie_instances(self, recommender):
        assert all(isinstance(m, Movie) for m in recommender.movies)

    def test_first_movie_title(self, recommender):
        assert recommender.movies[0].title == "Movie A"


class TestRecommendByGenre:
    def test_action_returns_three(self, recommender):
        results = recommender.recommend_by_genre("Action")
        assert len(results) == 3

    def test_action_sorted_by_rating(self, recommender):
        results = recommender.recommend_by_genre("Action")
        assert [m.title for m in results] == ["Movie C", "Movie A", "Movie E"]

    def test_top_n_limits_results(self, recommender):
        results = recommender.recommend_by_genre("Action", top_n=2)
        assert len(results) == 2
        assert results[0].title == "Movie C"

    def test_case_insensitive(self, recommender):
        lower = recommender.recommend_by_genre("action")
        upper = recommender.recommend_by_genre("Action")
        assert [m.title for m in lower] == [m.title for m in upper]

    def test_unknown_genre_returns_empty(self, recommender):
        assert recommender.recommend_by_genre("Horror") == []


class TestRecommendByYear:
    def test_year_2010_returns_movie_a(self, recommender):
        results = recommender.recommend_by_year(2010)
        assert len(results) == 1
        assert results[0].title == "Movie A"

    def test_year_1985_returns_movie_c(self, recommender):
        results = recommender.recommend_by_year(1985)
        assert len(results) == 1
        assert results[0].title == "Movie C"

    def test_top_n_limits_results(self, recommender):
        results = recommender.recommend_by_year(2010, top_n=1)
        assert len(results) == 1

    def test_unknown_year_returns_empty(self, recommender):
        assert recommender.recommend_by_year(1900) == []


class TestRecommendByDecade:
    def test_decade_2010s_returns_movie_a(self, recommender):
        results = recommender.recommend_by_decade("2010s")
        assert len(results) == 1
        assert results[0].title == "Movie A"

    def test_decade_1980s_returns_movie_c(self, recommender):
        results = recommender.recommend_by_decade("1980s")
        assert len(results) == 1
        assert results[0].title == "Movie C"

    def test_top_n_limits_results(self, recommender):
        results = recommender.recommend_by_decade("2010s", top_n=1)
        assert len(results) == 1

    def test_unknown_decade_returns_empty(self, recommender):
        assert recommender.recommend_by_decade("1890s") == []


class TestRecommendTopRated:
    def test_default_top5_order(self, recommender):
        results = recommender.recommend_top_rated()
        assert [m.title for m in results] == ["Movie C", "Movie A", "Movie E", "Movie B", "Movie D"]

    def test_top_n_three(self, recommender):
        results = recommender.recommend_top_rated(top_n=3)
        assert [m.title for m in results] == ["Movie C", "Movie A", "Movie E"]

    def test_top_n_one(self, recommender):
        results = recommender.recommend_top_rated(top_n=1)
        assert results[0].title == "Movie C"


class TestStreamMovies:
    def test_is_generator(self, recommender):
        import types
        assert isinstance(recommender.stream_movies(), types.GeneratorType)

    def test_yields_all_movies(self, recommender):
        streamed = list(recommender.stream_movies())
        assert len(streamed) == 5

    def test_all_items_are_movie_instances(self, recommender):
        assert all(isinstance(m, Movie) for m in recommender.stream_movies())

    def test_titles_match_loaded_order(self, recommender):
        streamed = list(recommender.stream_movies())
        assert [m.title for m in streamed] == ["Movie A", "Movie B", "Movie C", "Movie D", "Movie E"]


class TestGetAllGenres:
    def test_returns_set(self, recommender):
        assert isinstance(recommender.get_all_genres(), set)

    def test_exact_genres(self, recommender):
        assert recommender.get_all_genres() == {"Action", "Drama", "Comedy", "Thriller", "Romance"}

    def test_genre_count(self, recommender):
        assert len(recommender.get_all_genres()) == 5


class TestRecommendByMultipleGenres:
    def test_action_and_drama_returns_movie_a(self, recommender):
        results = recommender.recommend_by_multiple_genres("Action", "Drama")
        assert len(results) == 1
        assert results[0].title == "Movie A"

    def test_action_and_comedy_returns_movie_e(self, recommender):
        results = recommender.recommend_by_multiple_genres("Action", "Comedy")
        assert len(results) == 1
        assert results[0].title == "Movie E"

    def test_no_intersection_returns_empty(self, recommender):
        results = recommender.recommend_by_multiple_genres("Drama", "Romance")
        assert results == []

    def test_top_n_respected(self, recommender):
        results = recommender.recommend_by_multiple_genres("Action", "Drama", top_n=1)
        assert len(results) == 1


class TestRecursiveTopN:
    def test_top_three(self, recommender):
        results = recommender._recursive_top_n(recommender.movies, 3)
        assert [m.title for m in results] == ["Movie C", "Movie A", "Movie E"]

    def test_n_zero_returns_empty(self, recommender):
        assert recommender._recursive_top_n(recommender.movies, 0) == []

    def test_empty_list_returns_empty(self, recommender):
        assert recommender._recursive_top_n([], 3) == []

    def test_full_list_matches_top_rated(self, recommender):
        recursive = recommender._recursive_top_n(recommender.movies, 5)
        top_rated = recommender.recommend_top_rated(5)
        assert [m.title for m in recursive] == [m.title for m in top_rated]


class TestRecommendRandom:
    def test_returns_list(self, recommender):
        assert isinstance(recommender.recommend_random(3), list)

    def test_correct_length(self, recommender):
        assert len(recommender.recommend_random(3)) == 3

    def test_all_movie_instances(self, recommender):
        assert all(isinstance(m, Movie) for m in recommender.recommend_random(3))

    def test_results_from_movie_pool(self, recommender):
        titles = {m.title for m in recommender.movies}
        for m in recommender.recommend_random(5):
            assert m.title in titles

    def test_n_exceeds_pool_returns_all(self, recommender):
        results = recommender.recommend_random(100)
        assert len(results) == 5


class TestGetMoviePairs:
    def test_three_movies_give_three_pairs(self, recommender):
        pairs = recommender.get_movie_pairs(top_n=3)
        assert len(pairs) == 3

    def test_each_pair_is_two_tuple_of_movies(self, recommender):
        for pair in recommender.get_movie_pairs(top_n=3):
            assert isinstance(pair, tuple)
            assert len(pair) == 2
            assert all(isinstance(m, Movie) for m in pair)

    def test_two_movies_give_one_pair(self, recommender):
        pairs = recommender.get_movie_pairs(top_n=2)
        assert len(pairs) == 1


class TestGetTitles:
    def test_returns_list(self, recommender):
        assert isinstance(recommender.get_titles(), list)

    def test_correct_titles(self, recommender):
        assert recommender.get_titles() == ["Movie A", "Movie B", "Movie C", "Movie D", "Movie E"]

    def test_all_strings(self, recommender):
        assert all(isinstance(t, str) for t in recommender.get_titles())


class TestGetRatedAbove:
    def test_threshold_8_returns_three(self, recommender):
        results = recommender.get_rated_above(8.0)
        titles = {m.title for m in results}
        assert titles == {"Movie A", "Movie C", "Movie E"}

    def test_threshold_9_returns_one(self, recommender):
        results = recommender.get_rated_above(9.0)
        assert len(results) == 1
        assert results[0].title == "Movie C"

    def test_threshold_above_max_returns_empty(self, recommender):
        assert recommender.get_rated_above(10.0) == []

    def test_all_results_meet_threshold(self, recommender):
        threshold = 7.0
        for m in recommender.get_rated_above(threshold):
            assert m.rating >= threshold


class TestGetTitleRatingPairs:
    def test_returns_list_of_tuples(self, recommender):
        pairs = recommender.get_title_rating_pairs()
        assert isinstance(pairs, list)
        assert all(isinstance(p, tuple) for p in pairs)

    def test_correct_length(self, recommender):
        assert len(recommender.get_title_rating_pairs()) == 5

    def test_first_pair(self, recommender):
        assert recommender.get_title_rating_pairs()[0] == ("Movie A", 8.5)

    def test_each_pair_is_str_float(self, recommender):
        for title, rating in recommender.get_title_rating_pairs():
            assert isinstance(title, str)
            assert isinstance(rating, float)


class TestGetTotalRating:
    def test_correct_sum(self, recommender):
        assert recommender.get_total_rating() == pytest.approx(39.0)

    def test_returns_float(self, recommender):
        assert isinstance(recommender.get_total_rating(), float)


class TestGetGenreCounts:
    def test_returns_dict(self, recommender):
        assert isinstance(recommender.get_genre_counts(), dict)

    def test_action_count(self, recommender):
        assert recommender.get_genre_counts()["Action"] == 3

    def test_drama_count(self, recommender):
        assert recommender.get_genre_counts()["Drama"] == 2

    def test_comedy_count(self, recommender):
        assert recommender.get_genre_counts()["Comedy"] == 3

    def test_thriller_count(self, recommender):
        assert recommender.get_genre_counts()["Thriller"] == 1

    def test_romance_count(self, recommender):
        assert recommender.get_genre_counts()["Romance"] == 1

    def test_total_genre_keys(self, recommender):
        assert len(recommender.get_genre_counts()) == 5


class TestRecommendByGenreValidation:
    def test_empty_string_raises(self, recommender):
        with pytest.raises(ValueError):
            recommender.recommend_by_genre("")

    def test_whitespace_raises(self, recommender):
        with pytest.raises(ValueError):
            recommender.recommend_by_genre("   ")

    def test_non_string_raises(self, recommender):
        with pytest.raises(ValueError):
            recommender.recommend_by_genre(123)


class TestRecommendByYearValidation:
    def test_float_raises(self, recommender):
        with pytest.raises(ValueError):
            recommender.recommend_by_year(2010.0)

    def test_year_too_low_raises(self, recommender):
        with pytest.raises(ValueError):
            recommender.recommend_by_year(1800)

    def test_year_too_high_raises(self, recommender):
        with pytest.raises(ValueError):
            recommender.recommend_by_year(2200)

    def test_string_year_raises(self, recommender):
        with pytest.raises(ValueError):
            recommender.recommend_by_year("2010")


class TestGetRatingStats:
    # fixture ratings: [8.5, 7.0, 9.0, 6.5, 8.0]  mean=7.8, median=8.0, min=6.5, max=9.0
    def test_returns_dict(self, recommender):
        assert isinstance(recommender.get_rating_stats(), dict)

    def test_has_required_keys(self, recommender):
        assert set(recommender.get_rating_stats().keys()) == {'mean', 'median', 'std', 'min', 'max'}

    def test_mean(self, recommender):
        assert recommender.get_rating_stats()['mean'] == pytest.approx(7.8)

    def test_median(self, recommender):
        assert recommender.get_rating_stats()['median'] == pytest.approx(8.0)

    def test_min_max(self, recommender):
        stats = recommender.get_rating_stats()
        assert stats['min'] == pytest.approx(6.5)
        assert stats['max'] == pytest.approx(9.0)


class TestPlotRatingDistribution:
    def test_saves_file(self, recommender, tmp_path):
        out = tmp_path / "ratings.png"
        recommender.plot_rating_distribution(save_path=str(out))
        assert out.exists()

    def test_file_nonempty(self, recommender, tmp_path):
        out = tmp_path / "ratings.png"
        recommender.plot_rating_distribution(save_path=str(out))
        assert out.stat().st_size > 0

    def test_no_error_without_save(self, recommender):
        recommender.plot_rating_distribution()
