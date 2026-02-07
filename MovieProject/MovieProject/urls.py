from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect

# ===== views をファイル単位で明示的に import =====

# 最新映画一覧（肝心なページ）
from Movie.views.latest_movie_views import latest_movies

# TMDB 系
from Movie.views.tmdb_views import (
    tmdb_search,
    tmdb_discover,
    tmdb_movie_detail,
    tmdb_tv_detail,
    tmdb_person_detail,
    tmdb_person_works,
)

# 認証・ユーザー・コレクション系
from Movie.views.auth_views import (
    create_account,
    login_view,
    logout_view,
    movie_detail,
    my_subscriptions,
    collection_page,
    collection_detail,
    person_detail,
)

# ===== URL 設定 =====

urlpatterns = [
    # トップページ → 最新映画一覧
    path("", lambda request: redirect("/latest_movies/")),

    # 最新映画一覧（最重要）
    path("latest_movies/", latest_movies, name="latest_movies"),

    # 映画詳細（DB）
    path("movie/<int:movie_id>/", movie_detail, name="movie_detail"),

    # TMDB API
    path("api/tmdb/search/", tmdb_search, name="tmdb_search"),
    path("api/tmdb/discover/", tmdb_discover, name="tmdb_discover"),

    # コレクション・人物
    path("collection/<int:collection_id>/", collection_page, name="collection_page"),
    path("person/<int:person_id>/", person_detail, name="person_detail"),

    # TMDB 詳細 API
    path("api/movie/<int:id>/", tmdb_movie_detail, name="tmdb_movie_detail"),
    path("api/tv/<int:id>/", tmdb_tv_detail, name="tmdb_tv_detail"),
    path("api/collection/<int:collection_id>/", collection_detail, name="collection_detail"),
    path("api/person/<int:id>/", tmdb_person_detail, name="tmdb_person_detail"),
    path("api/person/<int:id>/credits/", tmdb_person_works, name="tmdb_person_works"),

    # サブスクリプション
    path("subscriptions/", my_subscriptions, name="my_subscriptions"),
    path("subscriptions/add/", my_subscriptions, name="add_subscription"),

    # 認証
    path("create_account/", create_account, name="create_account"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # 管理画面
    path("admin/", admin.site.urls),
]
