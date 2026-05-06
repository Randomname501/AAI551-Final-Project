from modules.movie import Movie
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import itertools
from functools import reduce


class Recommender:
    """
    A movie recommender system that loads a MovieLens dataset and suggests
    films based on genre, year, decade, rating, or combinations thereof.
    Composed of Movie objects produced during data loading.
    """

    def __init__(self, movies_path: str, ratings_path: str):
        """Initializes the Recommender by loading movies and ratings from CSV files."""
        try:
            self.movies = self.load_data(movies_path, ratings_path)
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"Error loading data: {e}")

    def load_data(self, movies_path: str, ratings_path: str) -> list:
        """
        Loads movie data from MovieLens CSVs, merges with average ratings,
        and constructs Movie objects using map for a functional data pipeline.
        """
        movies_df = pd.read_csv(movies_path)
        ratings_df = pd.read_csv(ratings_path)
        avg_ratings = ratings_df.groupby('movieId')['rating'].mean()
        movies_df['avg_rating'] = movies_df['movieId'].map(avg_ratings).fillna(0.0)
        # map transforms each row dict into a Movie object without an explicit loop
        return list(map(
            lambda row: Movie(row['movieId'], row['title'], row['genres'], row['avg_rating']),
            movies_df.to_dict('records')
        ))

    def rank_results(self, movies: list, header: str = "Top Results") -> str:
        """
        Formats a numbered list of movie recommendations using enumerate.
        Returns a multi-line string ready to print, with ranks starting at 1.
        """
        lines = [header]
        for rank, movie in enumerate(movies, start=1):
            lines.append(f"  {rank}. {movie}")
        return "\n".join(lines)

    def recommend_by_genre(self, genre: str, top_n: int = 5) -> list:
        """
        Recommends the top-rated movies matching a genre (case-insensitive).
        Raises ValueError for blank or non-string genre inputs.
        """
        if not isinstance(genre, str) or not genre.strip():
            raise ValueError("genre must be a non-empty string")
        filtered = [m for m in self.movies if any(genre.lower() in g.lower() for g in m.genre)]
        filtered.sort(key=lambda m: m.rating, reverse=True)
        return filtered[:top_n]

    def recommend_by_year(self, year: int, top_n: int = 5) -> list:
        """
        Recommends top-rated movies released in the given year.
        Raises ValueError if year is not an integer in the valid film era (1888-2100).
        """
        if not isinstance(year, int) or not (1888 <= year <= 2100):
            raise ValueError("year must be an integer between 1888 and 2100")
        filtered = [m for m in self.movies if m.year == year]
        filtered.sort(key=lambda m: m.rating, reverse=True)
        return filtered[:top_n]

    def recommend_by_decade(self, decade: str, top_n: int = 5) -> list:
        """
        Recommends top-rated movies from a given decade (e.g. '1990s').
        Strips the trailing 's' to recover the base year for decade comparison.
        """
        decade_year = int(decade.rstrip('s'))
        filtered = [m for m in self.movies if (m.year // 10) * 10 == decade_year]
        filtered.sort(key=lambda m: m.rating, reverse=True)
        return filtered[:top_n]

    def recommend_top_rated(self, top_n: int = 5, min_rating: float = 0.0) -> list:
        """
        Recommends the highest-rated movies, optionally above a minimum rating threshold.
        Uses filter with a lambda to exclude movies below the threshold before sorting.
        """
        eligible = list(filter(lambda m: m.rating >= min_rating, self.movies))
        return sorted(eligible, key=lambda m: m.rating, reverse=True)[:top_n]

    def recommend_by_multiple_genres(self, genre1: str, genre2: str, top_n: int = 5) -> list:
        """Returns movies belonging to BOTH genres using set intersection."""
        set1 = {m for m in self.movies if any(genre1.lower() in g.lower() for g in m.genre)}
        set2 = {m for m in self.movies if any(genre2.lower() in g.lower() for g in m.genre)}
        common = set1 & set2
        return sorted(common, key=lambda m: m.rating, reverse=True)[:top_n]

    def recommend_random(self, n: int = 5) -> list:
        """Returns n randomly selected movies using random.sample."""
        return random.sample(self.movies, min(n, len(self.movies)))

    def get_movie_pairs(self, top_n: int = 6) -> list:
        """
        Returns all pairwise combinations of the top-n movies using itertools.combinations.
        Useful for suggesting co-watch pairs from the highest-rated titles.
        """
        top = self.recommend_top_rated(top_n)
        return list(itertools.combinations(top, 2))

    def stream_movies(self, predicate=None):
        """
        Yields movies one at a time as a generator, optionally filtered by a predicate.
        Using a generator avoids building a full list in memory when only scanning is needed.
        """
        for movie in self.movies:
            if predicate is None or predicate(movie):
                yield movie

    def get_all_genres(self) -> set:
        """Returns the set of all unique genres across the dataset using a set comprehension."""
        return {genre for movie in self.movies for genre in movie.genre}

    def get_genre_counts(self) -> dict:
        """Returns a dict mapping each genre to the number of movies in it via dict comprehension."""
        all_genres = self.get_all_genres()
        return {genre: sum(1 for m in self.movies if genre in m.genre)
                for genre in all_genres}

    def _recursive_top_n(self, movies: list, n: int) -> list:
        """
        Recursively builds a top-n list by pulling the highest-rated movie each call.
        Base cases: n reaches 0, or the candidate list is empty.
        """
        if n == 0 or not movies:
            return []
        best = max(movies, key=lambda m: m.rating)
        remaining = [m for m in movies if m != best]
        return [best] + self._recursive_top_n(remaining, n - 1)

    def get_rating_stats(self) -> dict:
        """
        Returns mean, median, std, min, max, and total of all movie ratings.
        zip pairs stat names with numpy functions for a concise, data-driven dispatch.
        reduce independently sums all ratings so the caller can cross-check the mean.
        """
        ratings = np.array([m.rating for m in self.movies])
        stat_names = ['mean', 'median', 'std', 'min', 'max']
        stat_funcs = [np.mean, np.median, np.std, np.min, np.max]
        stats = {name: float(fn(ratings)) for name, fn in zip(stat_names, stat_funcs)}
        # reduce sums all ratings independently of numpy for auditability
        stats['total'] = round(reduce(lambda acc, m: acc + m.rating, self.movies, 0.0), 4)
        return stats

    def plot_rating_distribution(self, save_path: str | None = None, show: bool = False):
        """Plots a histogram of movie ratings with mean and median reference lines."""
        ratings = [m.rating for m in self.movies]
        fig, ax = plt.subplots()
        ax.hist(ratings, bins=10, range=(0, 10), edgecolor='black')
        ax.set_title('Movie Rating Distribution')
        ax.set_xlabel('Rating')
        ax.set_ylabel('Number of Movies')
        mean_val = float(np.mean(ratings))
        median_val = float(np.median(ratings))
        ax.axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:.2f}')
        ax.axvline(median_val, color='green', linestyle='--', label=f'Median: {median_val:.2f}')
        ax.legend()
        if save_path:
            fig.savefig(save_path)
        if show:
            plt.show()
        plt.close(fig)


if __name__ == "__main__":
    r = Recommender('data/ml-latest-small/movies.csv', 'data/ml-latest-small/ratings.csv')
    print(f"Loaded {len(r.movies)} movies.")
    print(r.rank_results(r._recursive_top_n(r.movies, 5), header="Top 5 (recursive):"))
    print("All genres:", r.get_all_genres())
    stats = r.get_rating_stats()
    print(f"Stats -- mean: {stats['mean']:.3f}, total: {stats['total']}")
