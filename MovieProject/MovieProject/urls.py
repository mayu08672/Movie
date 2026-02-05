from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect

# ✅ 正しい views の import
from MovieProject.Movie.views.auth_views import (
    latest_movies,               # ← latest_movies じゃない
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
    path('', lambda request: redirect('/login/')),

    # 🔽 latest_movies → latest に統一
    path("latest_movies/", latest_movies, name="latest_movies"),

    path('movie/<int:movie_id>/', movie_detail, name='movie_detail'),

    path("api/tmdb/search/", tmdb_search, name="tmdb_search"),
    path("api/tmdb/discover/", tmdb_discover, name="tmdb_discover"),

    path("collection/<int:collection_id>/", collection_page, name="collection_page"),
    path('person/<int:person_id>/', person_detail, name='person_detail'),

    path("api/movie/<int:id>/", tmdb_movie_detail, name="tmdb_movie_detail"),
    path("api/tv/<int:id>/", tmdb_tv_detail, name="tmdb_tv_detail"),
    path("api/collection/<int:collection_id>/", collection_detail, name="collection_detail"),
    path("api/person/<int:id>/", tmdb_person_detail, name="tmdb_person_detail"),
    path("api/person/<int:id>/credits/", tmdb_person_works, name="tmdb_person_works"),

    path("subscriptions/", my_subscriptions, name="my_subscriptions"),
    path('subscriptions/add/', my_subscriptions, name='add_subscription'),

    path('create_account/', create_account, name='create_account'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('admin/', admin.site.urls),
]
