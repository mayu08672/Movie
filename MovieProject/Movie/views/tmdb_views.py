import os
import requests
from django.http import JsonResponse
from django.conf import settings

TMDB_HEADERS = {
    "Authorization": f"Bearer {settings.TMDB_ACCESS_TOKEN}",
    "Accept": "application/json",
}

# -------------------------
# 🔍 1. search 用 API
# /api/tmdb/search/?query=xxx&type=movie
# -------------------------
def tmdb_search(request):
    query = request.GET.get("query", "")
    type_ = request.GET.get("type", "movie")

    if not query:
        return JsonResponse({"results": []})

    url = f"https://api.themoviedb.org/3/search/{type_}"
    params = {
        "query": query,
        "language": "ja-JP",
        "page": 1,
    }

    res = requests.get(url, headers=TMDB_HEADERS, params=params)

    if res.status_code != 200:
        return JsonResponse({"results": []})

    return JsonResponse(res.json())


# -------------------------
# 🎛 2. discover 用 API
# /api/tmdb/discover/?type=movie&genre=28&provider=8
# -------------------------
def tmdb_discover(request):
    type_ = request.GET.get("type", "movie")
    genre = request.GET.get("genre", "")
    provider = request.GET.get("provider", "")

    url = f"https://api.themoviedb.org/3/discover/{type_}"
    params = {
        "language": "ja-JP",
        "page": 1,
    }

    

    if genre:
        params["with_genres"] = genre

    if provider:
        params["with_watch_providers"] = provider
        params["watch_region"] = "JP"

    res = requests.get(url, headers=TMDB_HEADERS, params=params)

    if res.status_code != 200:
        return JsonResponse({"results": []})

    return JsonResponse(res.json())

# -------------------------
# 🎬 映画の詳細 API
# /api/tmdb/movie/<id>/
# -------------------------
def tmdb_movie_detail(request, id):
    detail_url = f"https://api.themoviedb.org/3/movie/{id}"
    credits_url = f"https://api.themoviedb.org/3/movie/{id}/credits"
    providers_url = f"https://api.themoviedb.org/3/movie/{id}/watch/providers"

    params = { "language": "ja-JP" }

    detail = requests.get(detail_url, headers=TMDB_HEADERS, params=params).json()
    credits = requests.get(credits_url, headers=TMDB_HEADERS, params=params).json()
    providers = requests.get(providers_url, headers=TMDB_HEADERS).json()

    return JsonResponse({
        "detail": detail,
        "credits": credits,
        "providers": providers,
    })

# -------------------------
# 📺 TV(ドラマ) の詳細 API
# /api/tmdb/tv/<id>/
# -------------------------
def tmdb_tv_detail(request, id):
    detail_url = f"https://api.themoviedb.org/3/tv/{id}"
    credits_url = f"https://api.themoviedb.org/3/tv/{id}/credits"
    providers_url = f"https://api.themoviedb.org/3/tv/{id}/watch/providers"

    params = { "language": "ja-JP" }

    detail = requests.get(detail_url, headers=TMDB_HEADERS, params=params).json()
    credits = requests.get(credits_url, headers=TMDB_HEADERS, params=params).json()
    providers = requests.get(providers_url, headers=TMDB_HEADERS).json()

    return JsonResponse({
        "detail": detail,
        "credits": credits,
        "providers": providers,
    })

# -------------------------
# 🧑 Person の詳細 API
# /api/tmdb/person/<id>/
# -------------------------
def tmdb_person_detail(request, id):
    detail_url = f"https://api.themoviedb.org/3/person/{id}"
    credits_url = f"https://api.themoviedb.org/3/person/{id}/combined_credits"

    params = { "language": "ja-JP" }

    detail = requests.get(detail_url, headers=TMDB_HEADERS, params=params).json()
    credits = requests.get(credits_url, headers=TMDB_HEADERS, params=params).json()

    return JsonResponse({
        "detail": detail,
        "credits": credits,
    })

def tmdb_person_works(request, id):
    url = f"https://api.themoviedb.org/3/person/{id}/combined_credits"
    params = { "language": "ja-JP" }

    res = requests.get(url, headers=TMDB_HEADERS, params=params)

    return JsonResponse(res.json())
