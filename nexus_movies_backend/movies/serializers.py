from rest_framework import serializers
from .models import Movie, Favorite

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'tmdb_id', 'title', 'overview', 'poster_path', 
                 'backdrop_path', 'release_date', 'vote_average', 'vote_count', 
                 'genre_ids', 'created_at']

class FavoriteSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'movie', 'created_at']
