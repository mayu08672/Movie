from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from Movie import views
from Movie.views.person_detail_views import person_detail


urlpatterns = [
    path('', lambda request: redirect('latest_movies')),

    path('latest_movies/', views.latest_movies, name='latest_movies'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('tv/<int:tv_id>/', views.tv_detail, name='tv_detail'),

    path("collection/<int:collection_id>/", views.collection_page, name="collection_page"),
    path("api/collection/<int:collection_id>/", views.collection_detail),

    path("api/tmdb/search/", views.tmdb_search, name='tmdb_search'),
    path("api/tmdb/discover/", views.tmdb_discover),

    path("person/<int:person_id>/", person_detail, name="person_detail"),

    path("api/movie/<int:id>/", views.tmdb_movie_detail),
    path("api/tv/<int:id>/", views.tmdb_tv_detail),
    path("api/person/<int:id>/", views.tmdb_person_detail),
    path("api/person/<int:id>/credits/", views.tmdb_person_works),

    path("subscriptions/", views.my_subscriptions, name="my_subscriptions"),
    path("subscriptions/add/", views.my_subscriptions, name="add_subscription"),

    path('create_account/', views.create_account, name='create_account'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('admin/', admin.site.urls),
]
