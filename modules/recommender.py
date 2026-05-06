from modules.movie import Movie
import pandas as pd
import random
import itertools
from functools import reduce

class Recommender:
    """
    A recommender system that loads data and suggests movies based on criteria
    """

    def __init__(self, filepath: str):
        try:
            self.movies = self.load_data(filepath)
        except FileNotFoundError:
            print(f"File not found: {filepath}")
        except Exception as e:
            print(f"Error loading data: {e}")   

    def load_data(self, filepath: str):
        """
        Loads movie data from a CSV file using pandas and creates Movie objects
        """
        df = pd.read_csv(filepath)
        movies = []
        for _, row in df.iterrows():
            movies.append(Movie(*row))
        return movies

    def recommend_by_genre(self, genre: str, top_n: int = 5):
        """
        Recommends top movies by genre based on rating
        """
        filtered = [m for m in self.movies if any(genre.lower() in g.lower() for g in m.genre)]
        filtered.sort(key=lambda m: m.rating, reverse=True)
        return filtered[:top_n]

    def recommend_by_director(self, director: str, top_n: int = 5):
        """
        Reccommends top movies by director based on rating
        """
        filtered = [m for m in self.movies if director.lower() in m.director.lower()]
        filtered.sort(key=lambda m: m.rating, reverse=True)
        return filtered[:top_n]

    def recommend_by_actor(self, actor: str, top_n: int = 5):
        """
        Recommends top movies by actor based on rating
        """
        filtered = [m for m in self.movies if any(actor.lower() in a.lower() for a in m.actors)]
        filtered.sort(key=lambda m: m.rating, reverse=True)
        return filtered[:top_n]

    def recommend_top_rated(self, top_n: int = 5):
        """
        Recommends top rated movies
        """
        sorted_movies = sorted(self.movies, key=lambda m: m.rating, reverse=True)
        return sorted_movies[:top_n]

    # --- Generator function (Requirement 4) ---
    def stream_movies(self):
        """Yields movies one at a time as a generator."""
        for movie in self.movies:
            yield movie

    # --- Set operations (Requirement 5) ---
    def get_all_genres(self):
        """Returns the set of all unique genres using a set comprehension."""
        return {genre for movie in self.movies for genre in movie.genre}

    def recommend_by_multiple_genres(self, genre1: str, genre2: str, top_n: int = 5):
        """Returns movies belonging to BOTH genres using set intersection."""
        set1 = {m for m in self.movies if any(genre1.lower() in g.lower() for g in m.genre)}
        set2 = {m for m in self.movies if any(genre2.lower() in g.lower() for g in m.genre)}
        common = set1 & set2
        return sorted(common, key=lambda m: m.rating, reverse=True)[:top_n]

    # --- Recursion (Requirement 6) ---
    def _recursive_top_n(self, movies, n):
        """Recursively builds a top-n list by pulling the highest-rated movie each call."""
        if n == 0 or not movies:
            return []
        best = max(movies, key=lambda m: m.rating)
        remaining = [m for m in movies if m != best]
        return [best] + self._recursive_top_n(remaining, n - 1)

    # --- Built-in libraries: random + itertools (Requirement 3) ---
    def recommend_random(self, n: int = 5):
        """Returns n randomly selected movies using the random module."""
        return random.sample(self.movies, min(n, len(self.movies)))

    def get_movie_pairs(self, top_n: int = 6):
        """Returns all pairs of top movies using itertools.combinations."""
        top = self.recommend_top_rated(top_n)
        return list(itertools.combinations(top, 2))

    # --- Special functions: map, filter, zip, reduce (Requirement 1) ---
    def get_titles(self):
        """Returns all movie titles using map and lambda."""
        return list(map(lambda m: m.title, self.movies))

    def get_rated_above(self, threshold: float):
        """Returns movies rated above a threshold using filter and lambda."""
        return list(filter(lambda m: m.rating >= threshold, self.movies))

    def get_title_rating_pairs(self):
        """Pairs each title with its rating using zip."""
        return list(zip(map(lambda m: m.title, self.movies),
                        map(lambda m: m.rating, self.movies)))

    def get_total_rating(self):
        """Sums all ratings using reduce."""
        return reduce(lambda acc, m: acc + m.rating, self.movies, 0.0)

    # --- Dict comprehension (Requirement 2) ---
    def get_genre_counts(self):
        """Returns {genre: count} using a dict comprehension."""
        all_genres = self.get_all_genres()
        return {genre: sum(1 for m in self.movies if genre in m.genre)
                for genre in all_genres}


# --- __name__ guard (Requirement 7) ---
if __name__ == "__main__":
    r = Recommender('data/movies.csv')
    print(f"Loaded {len(r.movies)} movies.")
    print("Top 3 (recursive):", [m.title for m in r._recursive_top_n(r.movies, 3)])
    print("All genres:", r.get_all_genres())
