# Movie Recommender System — AAI551 Final Project

## Project Description

A Python-based movie recommender system built on the [MovieLens ml-latest-small](https://grouplens.org/datasets/movielens/) dataset (9,742 movies, 100,836 ratings). The system loads real user ratings, computes per-movie averages, and exposes a set of recommendation and filtering methods through an interactive Jupyter notebook.

Users can explore the dataset through six live-updating widget panels — searching by title, filtering by genre, release year, decade, multi-genre intersection, and minimum rating — all without writing any code.

### Key Features

- Interactive Jupyter notebook with `ipywidgets` controls (dropdowns, sliders, live text search)
- Recommendations by genre, year, decade, rating threshold, and genre intersection
- Statistical analysis of ratings using `numpy` (mean, median, std, min, max)
- Rating distribution histogram with `matplotlib`
- Clean two-class design: `Movie` (data model) and `Recommender` (logic layer)
- 113 unit tests across both classes using `pytest`

---

## Team Members

| Name | Email | CWID |
|---|---|---|
| Suprith Reddy | sreddy4@stevens.edu | 2001010 |
| Yihan Jiang | jiang68@stevens.edu | 20015192 |

---

## File Structure

```
AAI551-Final-Project/
├── README.md
├── main.ipynb                       Interactive Jupyter notebook
├── data/
│   └── ml-latest-small/
│       ├── movies.csv               9,742 movies (movieId, title, genres)
│       └── ratings.csv              100,836 ratings (userId, movieId, rating, timestamp)
├── modules/
│   ├── __init__.py
│   ├── movie.py                     Movie class
│   └── recommender.py               Recommender class
└── tests/
    ├── conftest.py                  Shared pytest fixtures
    ├── test_movie.py                Movie unit tests (36 tests)
    └── test_recommender.py          Recommender unit tests (77 tests)
```

### Module Descriptions

**`modules/movie.py`** — `Movie` class  
Represents a single movie record parsed from the MovieLens CSV. Extracts year from title using regex, splits the pipe-separated genre string into a list, and stores a float average rating. Implements `__str__`, `__eq__`, `__hash__`, and `__getattr__` (dynamically computes `movie.decade` and `movie.is_classic` from the year field).

**`modules/recommender.py`** — `Recommender` class  
Loads the two CSV files with `pandas`, merges average ratings per movie, and creates a list of `Movie` objects. Provides recommendation methods (by genre, year, decade, top-rated, multi-genre intersection, random), functional utilities (map, filter, zip, reduce), a generator (`stream_movies`), recursive top-N selection, numpy statistics, and a matplotlib histogram.

---

## Dependencies

| Package | Purpose |
|---|---|
| `pandas` | CSV loading and rating aggregation |
| `numpy` | Rating statistics (mean, median, std, min, max) |
| `matplotlib` | Rating distribution histogram |
| `ipywidgets` | Interactive notebook controls |
| `pytest` | Unit testing |

Python 3.10 or later is required. Python 3.12 is recommended.

### Installation

```bash
pip install pandas numpy matplotlib ipywidgets pytest
```

---

## How to Run

### Interactive Notebook

1. Install Jupyter if not already installed:

   ```bash
   pip install jupyter
   ```

2. Launch from the project root:

   ```bash
   jupyter notebook
   ```

3. Open `main.ipynb` and run **Kernel → Restart & Run All**.

The notebook is organized into three sections:

- **Interactive Movie Explorer** — Six widget panels that update results in real time:
  - *Search by Title* — type any fragment to find matching movies
  - *Filter by Genre* — dropdown of all 19 genres + result count slider
  - *Filter by Release Year* — slider from 1902 to 2018
  - *Filter by Decade* — dropdown of all decades in the dataset
  - *Two-Genre Intersection* — pick two genres to see movies in both
  - *Filter by Minimum Rating* — float slider from 0.0 to 5.0

- **Statistics & Visualization** — numpy summary statistics and a matplotlib rating histogram

- **Feature Demonstrations** — Static cells showing each required Python feature (`__getattr__`, generator, set operations, recursion, built-in libraries, map/filter/zip/reduce, dict comprehension)

### Running Tests

```bash
python -m pytest tests/
```

Run a specific file:

```bash
python -m pytest tests/test_movie.py
python -m pytest tests/test_recommender.py
```

On Windows if `python` is not on PATH:

```bash
py -m pytest tests/
```

---

## Python Features Demonstrated

| Requirement | Implementation |
|---|---|
| Classes with relationship | `Movie` (data model) composed inside `Recommender` |
| `__str__`, operator overload | `Movie.__str__`, `__eq__`, `__hash__` |
| `__getattr__` | `Movie.decade`, `Movie.is_classic` computed on demand |
| Two advanced libraries | `pandas` (data I/O), `numpy` (statistics), `matplotlib` (visualization) |
| Exception handling | `FileNotFoundError` on bad CSV path; `ValueError` on invalid genre/year input |
| Data I/O | `pd.read_csv` for both MovieLens files |
| Generators | `Recommender.stream_movies()` yields one `Movie` at a time |
| Set operations | `get_all_genres()` (set comprehension), `recommend_by_multiple_genres()` (set intersection `&`) |
| Recursion | `_recursive_top_n()` — base case on empty list or n=0 |
| Built-in libraries | `random` (sampling), `itertools` (combinations), `functools.reduce` |
| Comprehensions | List, set, and dict comprehensions throughout `recommender.py` |
| `map`, `filter`, `zip`, `reduce`, `lambda` | `get_titles`, `get_rated_above`, `get_title_rating_pairs`, `get_total_rating` |
| `__name__` guard | Bottom of `recommender.py` |
| Pytest | 113 tests across `test_movie.py` and `test_recommender.py` |

---

## Contributions

**Yihan Jiang**
- Designed and implemented `modules/movie.py`: `Movie` class with regex-based title/year parsing, genre splitting, `__str__`, `__eq__`, `__hash__`, and the `__getattr__` system for computed attributes (`decade`, `is_classic`)
- Wrote the README and project documentation

**Suprith Reddy**
- Designed and implemented `modules/recommender.py`: all recommendation methods, functional programming patterns (map, filter, zip, reduce, lambda), set operations, recursion, generator, numpy statistics, matplotlib visualization, `ValueError` input guards, and the `__name__` guard
- Built the interactive Jupyter notebook (`main.ipynb`) with six `ipywidgets` filter panels
- Wrote all 113 pytest test cases in `tests/conftest.py`, `tests/test_movie.py`, and `tests/test_recommender.py`
