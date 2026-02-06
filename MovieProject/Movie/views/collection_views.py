from django.http import JsonResponse
import requests
from django.shortcuts import render
from django.conf import settings


def collection_page(request, collection_id):
    return render(request, "collection_detail.html", {"collection_id": collection_id})


TMDB_HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {settings.TMDB_ACCESS_TOKEN}",
}


def collection_detail(request, collection_id):
    url = f"https://api.themoviedb.org/3/collection/{collection_id}"

    try:
        res = requests.get(url, headers=TMDB_HEADERS)
        data = res.json()

        # TMDB がエラーを返した
        if "status_code" in data:
            return JsonResponse(
                {"error": data.get("status_message", "TMDB API error")},
                status=res.status_code
            )

        return JsonResponse({"detail": data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)