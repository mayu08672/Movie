from django.shortcuts import render
import requests
from django.conf import settings

TMDB_HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {settings.TMDB_ACCESS_TOKEN}",
}

def person_detail(request, person_id):
    params = {"language": "ja-JP"}

    # ① 人物の基本情報
    url_detail = f"https://api.themoviedb.org/3/person/{person_id}"
    person_resp = requests.get(url_detail, headers=TMDB_HEADERS, params=params)
    person = person_resp.json()

    # ② 出演作（映画＋ドラマ）
    url_credits = f"https://api.themoviedb.org/3/person/{person_id}/combined_credits"
    credits_resp = requests.get(url_credits, headers=TMDB_HEADERS, params=params)
    works = credits_resp.json().get("cast", [])

    # 人気順に並べ替え
    works = sorted(works, key=lambda x: x.get("popularity", 0), reverse=True)
    works = works[:20]

    # ③ for の中に全部入れる！！！ ← ここが超重要
    for w in works:

        # URL
        if w.get("media_type") == "movie":
            w["detail_url"] = f"/movie/{w['id']}/"
        elif w.get("media_type") == "tv":
            w["detail_url"] = f"/tv/{w['id']}/"
        else:
            w["detail_url"] = "#"

        # タイトル（映画は title、ドラマは name）
        title = w.get("title") or w.get("name")
        w["title_jp"] = title if title else "タイトル不明"

        # ポスター
        poster = w.get("poster_path")
        if poster:
            w["poster_url"] = f"https://image.tmdb.org/t/p/w300{poster}"
        else:
            w["poster_url"] = "/static/20200505_noimage.png"

    return render(request, "person_detail.html", {
        "person": person,
        "works": works,
    })
