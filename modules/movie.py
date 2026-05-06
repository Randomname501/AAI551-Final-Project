import re


class Movie:
    """
    Creates a movie object with information about the movie
    """

    def __init__(self, movie_id, title, genres, avg_rating=0.0):
        self.movie_id = int(movie_id)
        year_match = re.search(r'\((\d{4})\)\s*$', title)
        self.year = int(year_match.group(1)) if year_match else 0
        self.title = re.sub(r'\s*\(\d{4}\)\s*$', '', title).strip()
        self.genre = [] if genres == "(no genres listed)" else genres.split('|')
        self.rating = float(avg_rating)

    def __str__(self):
        return f"{self.title} ({self.year}) is a {', '.join(self.genre)} movie with a rating of {self.rating}"

    def __eq__(self, other):
        if isinstance(other, Movie):
            return (self.title == other.title and self.year == other.year
                    and self.genre == other.genre and self.rating == other.rating)
        return False

    def __hash__(self):
        return hash(self.title)

    def __getattr__(self, name):
        if name == 'decade':
            return f"{(object.__getattribute__(self, 'year') // 10) * 10}s"
        if name == 'is_classic':
            return object.__getattribute__(self, 'year') < 1980
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
