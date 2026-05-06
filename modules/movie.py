class Movie:
    """
    Creates a movie object with information about the movie
    """

    def __init__(self, title, genre, director, rating):
        self.title = title
        self.genre = genre
        self.director = director
        self.rating = rating

    def __str__(self):
        return f"{self.title} is a {self.genre} movie directed by {self.director} with a rating of {self.rating}"
    
    def __eq__(self, other):
        if isinstance(other, Movie):
            return self.title == other.title and self.genre == other.genre and self.director == other.director and self.rating == other.rating
        return False
    
