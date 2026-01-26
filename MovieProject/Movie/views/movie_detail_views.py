from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.conf import settings

TMDB_HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {settings.TMDB_ACCESS_TOKEN}",
}

# サブスク名 → URL のマッピング
SUBSCRIPTION_URLS = {
    "Netflix": "https://www.netflix.com/jp/",
    "Amazon Prime Video": "https://www.amazon.co.jp/Prime-Video/b?ie=UTF8&node=3535604051",
    "Disney+": "https://www.disneyplus.com/ja-jp",
    "Hulu": "https://www.hulu.jp/",
    # 必要に応じて追加
}
def tv_detail(request, tv_id):
    # TV詳細情報
    url_detail = f"https://api.themoviedb.org/3/tv/{tv_id}"
    params = {"language": "ja-JP"}
    tv_resp = requests.get(url_detail, headers=TMDB_HEADERS, params=params)
    tv = tv_resp.json()

    # キャスト情報
    url_credits = f"https://api.themoviedb.org/3/tv/{tv_id}/credits"
    credits_resp = requests.get(url_credits, headers=TMDB_HEADERS, params=params)
    credits = credits_resp.json().get("cast", [])[:10]

    # サブスク情報（日本）
    url_providers = f"https://api.themoviedb.org/3/tv/{tv_id}/watch/providers"
    providers_resp = requests.get(url_providers, headers=TMDB_HEADERS)
    providers = providers_resp.json().get("results", {}).get("JP", {}).get("flatrate", [])

    for p in providers:
        p["url"] = SUBSCRIPTION_URLS.get(p["provider_name"], "#")

    return render(request, "movie_detail.html", {
        "tv": tv,
        "cast": credits,
        "providers": providers,
    })


def movie_detail(request, movie_id):
    # 映画詳細情報
    url_detail = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"language": "ja-JP"}
    movie_resp = requests.get(url_detail, headers=TMDB_HEADERS, params=params)
    movie = movie_resp.json()

    # キャスト情報
    url_credits = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    credits_resp = requests.get(url_credits, headers=TMDB_HEADERS, params=params)
    credits = credits_resp.json().get("cast", [])[:10]  # 上位10人だけ

    # サブスク情報（日本）
    url_providers = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"
    providers_resp = requests.get(url_providers, headers=TMDB_HEADERS)
    providers = providers_resp.json().get("results", {}).get("JP", {}).get("flatrate", [])

    # URL を追加
    for p in providers:
        p["url"] = SUBSCRIPTION_URLS.get(p["provider_name"], "#")

    return render(request, "movie_detail.html", {
        "movie": movie,
        "cast": credits,
        "providers": providers
    })



