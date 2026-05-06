class Movie:
    """
    Creates a movie object with information about the movie
    """

    def __init__(self, imdb_title_id, original_title, year, genre, duration, director, writer, production_company, actors, description, avg_vote, votes):
        self.title = original_title
        self.genre = genre
        self.director = director
        self.rating = float(avg_vote)
        self.year = int(year)
        self.actors = actors

    def __str__(self):
        return f"{self.title} is a {self.genre} movie directed by {self.director} with a rating of {self.rating}"
    
    def __eq__(self, other):
        if isinstance(other, Movie):
            return self.title == other.title and self.genre == other.genre and self.director == other.director and self.rating == other.rating
        return False
