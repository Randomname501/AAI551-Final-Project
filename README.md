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
python3 -m pip install pandas numpy pytest
```

## Running the Jupyter Notebook

For an interactive demonstration of the recommender system:

1. Install Jupyter if not already installed:

   ```bash
   pip install jupyter
   ```

2. Launch Jupyter Notebook from the project root:

   ```bash
   jupyter notebook
   ```

## Running Pytest

To run our test cases you would:

```bash
python -m pytest tests/test_recommender.py
python -m pytest tests/test_movie.py
```

## Contributions

- Yihan: Created movie.py and created README and documentation
- Suprith: Created Recommender.py and created test cases.
