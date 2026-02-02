# views.py

from django.shortcuts import render
import requests
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse

print("latest_movie_views START")


def tmdb_search(request):
    query = request.GET.get("query")
    search_type = request.GET.get("type", "movie")  # movie / tv / person

    if not query:
        return JsonResponse({"results": []})

    url = f"https://api.themoviedb.org/3/search/{search_type}"
    params = {
        "query": query,
        "language": "ja-JP",
        "page": 1,
        "include_adult": "false"
    }

    response = requests.get(url, headers=TMDB_HEADERS, params=params)

    if response.status_code != 200:
        return JsonResponse({"results": []})

    return JsonResponse({
        "results": response.json().get("results", [])
    })

print("before TMDB_HEADERS")

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

def tmdb_discover(request):
    media_type = request.GET.get("type", "movie")
    genre = request.GET.get("genre", "")
    provider = request.GET.get("provider", "")

    url = f"https://api.themoviedb.org/3/discover/{media_type}"

    params = {
        "language": "ja-JP",
        "sort_by": "popularity.desc"
    }

    if genre:
        params["with_genres"] = genre
    if provider:
        params["with_watch_providers"] = provider
        params["watch_region"] = "JP"

    res = requests.get(url, headers=TMDB_HEADERS, params=params)

    if res.status_code != 200:
        return JsonResponse({"results": []})

    return JsonResponse({"results": res.json().get("results", [])})
