# Movie Recommender System — AAI551 Final Project

## Project Description

A Python-based movie recommender system built on the [MovieLens ml-latest-small](https://grouplens.org/datasets/movielens/) dataset (9,742 movies, 100,836 ratings). The system loads real user ratings, computes per-movie averages, and exposes a set of recommendation and filtering methods through an interactive Jupyter notebook.

Users can explore the dataset through six live-updating widget panels — searching by title, filtering by genre, release year, decade, multi-genre intersection, and minimum rating — all without writing any code.

### Key Features

- Interactive Jupyter notebook with `ipywidgets` controls (dropdowns, sliders, live text search)
- Recommendations by genre, year, decade, rating threshold, genre intersection, and random sampling
- Numbered output via `rank_results` using `enumerate`; lazy streaming via `stream_movies(predicate)`
- Statistical analysis of ratings using `numpy` (mean, median, std, min, max, reduce-based total)
- Rating distribution histogram with `matplotlib` (mean and median reference lines)
- Clean two-class design: `Movie` (data model) and `Recommender` (logic layer)
- 113 unit tests across both classes using `pytest`

---

## Team Members

| Name | Email | CWID |
|---|---|---|
| Suprith Reddy | sreddy4@stevens.edu | 20010383 |
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
│   ├── __init__.py                  Exports Movie and Recommender
│   ├── movie.py                     Movie class
│   └── recommender.py               Recommender class
└── tests/
    ├── conftest.py                  Shared pytest fixtures
    ├── test_movie.py                Movie unit tests (40 tests)
    └── test_recommender.py          Recommender unit tests (73 tests)
```

### Module Descriptions

**`modules/movie.py`** — `Movie` class  
Represents a single movie record parsed from the MovieLens CSV. Extracts year from title using regex, splits the pipe-separated genre string into a list, and stores a float average rating. Implements `__str__`, `__eq__`, `__hash__`, `__len__` (number of genres), and `__getattr__` (dynamically computes `movie.decade` and `movie.is_classic` from the year field).

**`modules/recommender.py`** — `Recommender` class  
Loads the two CSV files with `pandas`, merges average ratings per movie, and constructs a list of `Movie` objects using `map` for a functional data pipeline. Provides recommendation methods (by genre, year, decade, top-rated with optional `min_rating` via `filter`, multi-genre intersection via set operations, random), `rank_results` (numbered output via `enumerate`), a lazy generator (`stream_movies(predicate)`), recursive top-N selection, numpy statistics (dispatched via `zip`, cross-checked via `reduce`), and a matplotlib histogram.

---

## Dependencies

| Package | Purpose |
|---|---|
| `pandas` | CSV loading and rating aggregation |
| `numpy` | Rating statistics (mean, median, std, min, max) |
| `matplotlib` | Rating distribution histogram |
| `ipywidgets` | Interactive notebook controls |
| `pytest` | Unit testing |

Python 3.12 or later is required.

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

3. Open `main.ipynb` and run **Kernel → Restart Kernel and Run All Cells**.

The notebook is organized into three sections:

**References used to learn widget development:**
- [Widget Custom](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20Custom.html) — ipywidgets documentation on building custom widgets
- [Style Guide (v7.6.3)](https://ipywidgets.readthedocs.io/en/7.6.3/examples/Widget%20Styling.html) — ipywidgets style guide

- **Interactive Movie Explorer** — Six widget panels that update results in real time:
  - *Search by Title* — type any fragment to find matching movies
  - *Filter by Genre* — dropdown of all 19 genres + result count slider
  - *Filter by Release Year* — slider from 1902 to 2018
  - *Filter by Decade* — dropdown of all decades in the dataset
  - *Two-Genre Intersection* — pick two genres to see movies in both
  - *Filter by Minimum Rating* — float slider (uses `filter` inside `recommend_top_rated`)

- **Statistics & Visualization** — numpy summary statistics (including `reduce`-based total) and a matplotlib rating histogram with mean/median reference lines

- **System Walkthrough** — Cells showing each Python feature in the context of the recommendation workflow (`rank_results`/`enumerate`, lazy `stream_movies(predicate)`, `zip`/`reduce` in stats, `__getattr__`, set operations, recursion, built-in libraries, dict comprehension)

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
| `__str__`, operator overloads | `Movie.__str__`, `__eq__`, `__hash__`, `__len__` (genre count) |
| `__getattr__` | `Movie.decade`, `Movie.is_classic` computed on demand |
| Two advanced libraries | `pandas` (data I/O + rating merge), `numpy` (statistics), `matplotlib` (histogram) |
| Exception handling | `FileNotFoundError` on bad CSV path; `ValueError` on invalid genre/year input |
| Data I/O | `pd.read_csv` for both MovieLens files |
| `map` | `load_data` — constructs `Movie` objects from DataFrame rows |
| `filter` + `lambda` | `recommend_top_rated(min_rating)` — excludes movies below threshold |
| `zip` | `get_rating_stats` — pairs stat names with numpy functions for dispatch |
| `reduce` | `get_rating_stats` — independently sums all ratings to cross-check the mean |
| `enumerate` | `rank_results` — numbers every recommendation list starting at 1 |
| Generator | `stream_movies(predicate)` — yields movies lazily, optionally filtered |
| Set operations | `get_all_genres()` (set comprehension), `recommend_by_multiple_genres()` (set `&`) |
| Recursion | `_recursive_top_n()` — base case on empty list or n=0 |
| Built-in libraries | `random` (sampling), `itertools` (co-watch pairs), `functools.reduce` |
| Comprehensions | List (filtered movies), set (`get_all_genres`), dict (`get_genre_counts`) |
| `__name__` guard | Bottom of `recommender.py` |
| Pytest | 113 tests in `test_movie.py` (40) and `test_recommender.py` (73) |

---

## Contributions

**Yihan Jiang**
- Designed and implemented `modules/movie.py`: `Movie` class with regex-based title/year parsing, genre splitting, `__str__`, `__eq__`, `__hash__`, `__len__`, and the `__getattr__` system for computed attributes (`decade`, `is_classic`)
- Wrote the README and project documentation

**Suprith Reddy**
- Designed and implemented `modules/recommender.py`: all recommendation methods, functional data pipeline (`map` in `load_data`), `filter` in `recommend_top_rated`, `zip`/`reduce` in `get_rating_stats`, `enumerate` in `rank_results`, lazy generator `stream_movies(predicate)`, set operations, recursion, numpy statistics, matplotlib visualization, `ValueError` input guards, and the `__name__` guard
- Built the interactive Jupyter notebook (`main.ipynb`) with six `ipywidgets` filter panels and system walkthrough cells
- Wrote all 113 pytest test cases in `tests/conftest.py`, `tests/test_movie.py`, and `tests/test_recommender.py`
