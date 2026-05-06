class Movie:
    """
    Creates a movie object with information about the movie
    """

    def __init__(self, imdb_title_id, original_title, year, genre, duration, director, writer, production_company, actors, description, avg_vote, votes):
        self.title = original_title
        self.genre = genre.split(', ')
        self.director = director
        self.rating = float(avg_vote)
        self.year = int(year)
        self.actors = actors.split(', ')

    def __str__(self):
        return f"{self.title} is a {', '.join(self.genre)} movie directed by {self.director} with a rating of {self.rating}"
    
    def __eq__(self, other):
        if isinstance(other, Movie):
            return self.title == other.title and self.genre == other.genre and self.director == other.director and self.rating == other.rating
        return False

    def __hash__(self):
        return hash(self.title)

    def __getattr__(self, name):
        if name == 'decade':
            return f"{(object.__getattribute__(self, 'year') // 10) * 10}s"
        if name == 'is_classic':
            return object.__getattribute__(self, 'year') < 1980
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
