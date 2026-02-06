"""
URL configuration for MovieProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Movie import views
from Movie.views import person_detail
from django.shortcuts import redirect
from Movie.views import tmdb_search

urlpatterns = [
    path('', lambda request: redirect('/login/')),  # ← これ追加！
    path('', views.latest_movies, name='latest_movies'),
    path('latest_movies/', views.latest_movies, name='latest_movies'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('tv/<int:tv_id>/', views.tv_detail, name='tv_detail'),
     # 削除
path("api/search/", tmdb_search, name="tmdb_search"),

    path("api/tmdb/discover/", views.tmdb_discover),
    # 削除する
path("person/<int:person_id>/", person_detail, name="person_detail"),

    path("api/movie/<int:id>/", views.tmdb_movie_detail),
    path("api/tv/<int:id>/", views.tmdb_tv_detail),
    path("api/person/<int:id>/", views.tmdb_person_detail),
    path("api/person/<int:id>/credits/", views.tmdb_person_works),

   
     # サブスク一覧ページ
    path("subscriptions/", views.my_subscriptions, name="my_subscriptions"),
    path('subscriptions/add/', views.my_subscriptions, name='add_subscription'),
    
    
  
    path('create_account/', views.create_account, name='create_account'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    

    path('admin/', admin.site.urls),
]
