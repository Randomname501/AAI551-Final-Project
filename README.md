# AAI551 Final Project

## Project Overview

Movie Recommender is a simple Python-based project that reads movie data and uses a basic recommender system to suggest movies based on attributes such as title, director, genre, and rating.

## Contributors

- Suprith Reddy — sreddy4@stevens.edu — CWID: 2001010
- Yihan Jiang — jiang68@stevens.edu — CWID: 20015192

## File Hierarchy

```
AAI551-Final-Project/
├── README.md
├── main.ipynb
├── data/
│   └── movies.csv
└── modules/
    ├── __init__.py
    ├── movie.py
    └── recommender.py
```

### Key files

- `main.ipynb` — Jupyter notebook for demonstration, experimentation, and model exploration.
- `data/movies.csv` — Dataset with movie metadata such as title, year, genre, director, cast, and ratings.
- `modules/movie.py` — `Movie` class representing a movie record.
- `modules/recommender.py` — Recommender class that loads movie data and provides recommendation methods.

## Dependencies

- Python 3.10+ (Python 3.12 recommended)
- pandas
- numpy

### Installation

```bash
python3 -m pip install pandas
python3 -m pip install numpy
```

If you are using the notebook, install Jupyter as well:

```bash
python3 -m pip install jupyter
```
