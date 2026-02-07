from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect

# latest_movies は専用ファイルから import
from Movie.views.latest_movie_views import latest_movies

# 認証・API・詳細系は auth_views から import
from Movie.views.auth_views import (
    tmdb_search,
    tmdb_discover,
    movie_detail,
    my_subscriptions,
    create_account,
    login_view,
    logout_view,
    collection_page,
    person_detail,
    tmdb_movie_detail,
    tmdb_tv_detail,
    collection_detail,
    tmdb_person_detail,
    tmdb_person_works,
)

urlpatterns = [
    # トップページは最新映画一覧へリダイレクト
    path('', lambda request: redirect('/latest_movies/')),

    # 最新映画一覧
    path("latest_movies/", latest_movies, name="latest_movies"),

    # 映画詳細（DB）
    path('movie/<int:movie_id>/', movie_detail, name='movie_detail'),

    # TMDB API
    path("api/tmdb/search/", tmdb_search, name="tmdb_search"),
    path("api/tmdb/discover/", tmdb_discover, name="tmdb_discover"),

    # コレクション・人物
    path("collection/<int:collection_id>/", collection_page, name="collection_page"),
    path('person/<int:person_id>/', person_detail, name='person_detail'),

    # TMDB 詳細 API
    path("api/movie/<int:id>/", tmdb_movie_detail, name="tmdb_movie_detail"),
    path("api/tv/<int:id>/", tmdb_tv_detail, name="tmdb_tv_detail"),
    path("api/collection/<int:collection_id>/", collection_detail, name="collection_detail"),
    path("api/person/<int:id>/", tmdb_person_detail, name="tmdb_person_detail"),
    path("api/person/<int:id>/credits/", tmdb_person_works, name="tmdb_person_works"),

    # サブスクリプション
    path("subscriptions/", my_subscriptions, name="my_subscriptions"),
    path('subscriptions/add/', my_subscriptions, name='add_subscription'),

    # 認証
    path('create_account/', create_account, name='create_account'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # 管理画面
    path('admin/', admin.site.urls),
]
