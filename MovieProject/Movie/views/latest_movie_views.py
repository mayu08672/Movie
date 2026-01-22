# views.py
from django.shortcuts import render
import requests
from datetime import datetime


TMDB_HEADERS = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjN2M4YTFiYTExYzk4MjM1ODczNjAyNjBlYjk5ZTUwNiIsIm5iZiI6MTc1OTgwODM3My43Nzc5OTk5LCJzdWIiOiI2OGU0OGI3NTI3ZTFjZDEyODU2MTgxM2QiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.L1lIlKJOH-YRL1zrBby86dVcn79QR1OTJUgzqOGsdno"
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
