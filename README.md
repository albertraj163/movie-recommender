# Movie Recommendation System

A professional web application for **user-based collaborative filtering** using cosine similarity. Built with Flask, pandas, and scikit-learn.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- **Collaborative filtering** — finds similar users via cosine similarity
- **Weighted recommendations** — predicts ratings from neighbor users
- **Professional UI** — dark cinema-themed dashboard with live stats
- **REST API** — `/api/users`, `/api/recommend/<user_id>`, and more
- **Expanded dataset** — 8 users, 15 movies, 40 ratings

## Project Structure

```
movie-recommender/
├── app.py                 # Flask web server
├── recommender.py         # Recommendation engine
├── movies.csv             # Movie metadata
├── sample_ratings.csv     # User ratings dataset
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Main UI
└── static/
    ├── css/style.css
    └── js/app.js
```

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the web app

```bash
python app.py
```

### 3. Open in browser

**Local URL:** [http://localhost:5050](http://localhost:5050)

The app runs on **port 5050** by default. To use a different port:

```bash
PORT=5000 python app.py
```

### CLI Demo (optional)

```bash
python recommender.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web UI |
| GET | `/api/stats` | Dataset statistics |
| GET | `/api/users` | List all users |
| GET | `/api/users/<id>/ratings` | User's rated movies |
| GET | `/api/recommend/<id>?top_n=5` | Personalized recommendations |

## How It Works

1. Build a user–movie rating matrix from the dataset
2. Compute cosine similarity between all user pairs
3. For a target user, find the most similar users
4. Recommend unwatched movies weighted by similarity × rating

## Tech Stack

- **Backend:** Python, Flask
- **ML:** scikit-learn (cosine similarity), pandas
- **Frontend:** HTML5, CSS3, Vanilla JavaScript

## Author

Albert Raj — [github.com/albertraj163](https://github.com/albertraj163)
