from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.get_movies, name='get_movies'),
    path('movies/search/', views.search_movies, name='search_movies'),
    path('movies/<int:movie_id>/', views.get_movie_details, name='movie_details'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorites/<int:movie_id>/', views.remove_favorite, name='remove_favorite'),
]
