from modules.movie import Movie
import pandas as pd

class Recommender:
    """
    A recommender system that loads data and suggests movies based on criteria
    """

    def __init__(self, filepath: str):
        self.movies = self.load_data(filepath)

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
        filtered = [m for m in self.movies if director.lower() in m.director.lower()]
        filtered.sort(key=lambda m: m.rating, reverse=True)
        return filtered[:top_n]

    def recommend_by_actor(self, actor: str, top_n: int = 5):
        filtered = [m for m in self.movies if any(actor.lower() in a.lower() for a in m.actors)]
        filtered.sort(key=lambda m: m.rating, reverse=True)
        return filtered[:top_n]

    def recommend_top_rated(self, top_n: int = 5):
        sorted_movies = sorted(self.movies, key=lambda m: m.rating, reverse=True)
        return sorted_movies[:top_n]