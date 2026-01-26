# views.py
from django.shortcuts import render
import requests
from datetime import datetime
from django.conf import settings

TMDB_HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {settings.TMDB_ACCESS_TOKEN}",
}

def latest_movies(request):
    url = "https://api.themoviedb.org/3/movie/now_playing"
    params = {
        "language": "ja-JP",
        "page": 1
    }

    response = requests.get(url, headers=TMDB_HEADERS, params=params)
    movies = []

    if response.status_code == 200:
        movies = response.json().get("results", [])

        # 公開日でソート（最新順）
        movies.sort(
            key=lambda x: x.get("release_date") or "0000-00-00",
            reverse=True
        )

        for movie in movies:
            movie["media_type"] = "movie"
            if movie.get("poster_path"):
                movie["poster_url"] = f"https://image.tmdb.org/t/p/w300{movie['poster_path']}"
            else:
                movie["poster_url"] = "/static/noimage.png"

    return render(request, "latest_movies.html", {"movies": movies})
