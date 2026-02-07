from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect

from Movie.views.latest_movie_views import latest_movies
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
    path("", lambda request: redirect("/login/")),
    path("latest_movies/", latest_movies, name="latest_movies"),
    path("movie/<int:movie_id>/", movie_detail, name="movie_detail"),
    path("api/tmdb/search/", tmdb_search),
    path("api/tmdb/discover/", tmdb_discover),
    path("collection/<int:collection_id>/", collection_page),
    path("person/<int:person_id>/", person_detail),
    path("api/movie/<int:id>/", tmdb_movie_detail),
    path("api/tv/<int:id>/", tmdb_tv_detail),
    path("api/collection/<int:collection_id>/", collection_detail),
    path("api/person/<int:id>/", tmdb_person_detail),
    path("api/person/<int:id>/credits/", tmdb_person_works),
    path("subscriptions/", my_subscriptions),
    path("subscriptions/add/", my_subscriptions),
    path("create_account/", create_account, name="create_account"),

    path("login/", login_view),
    path("logout/", logout_view),
    path("admin/", admin.site.urls),
]
