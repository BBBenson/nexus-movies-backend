import requests
from django.conf import settings
from .models import Movie

class TMDBService:
    BASE_URL = "https://api.themoviedb.org/3"
    
    @classmethod
    def get_headers(cls):
        return {
            'Authorization': f'Bearer {settings.TMDB_API_KEY}',
            'Content-Type': 'application/json'
        }
    
    @classmethod
    def fetch_movies(cls, endpoint, params=None):
        """Fetch movies from TMDB API"""
        url = f"{cls.BASE_URL}/{endpoint}"
        response = requests.get(url, headers=cls.get_headers(), params=params)
        
        if response.status_code == 200:
            data = response.json()
            movies = []
            
            for movie_data in data.get('results', []):
                # Create or update movie in database
                movie, created = Movie.objects.get_or_create(
                    tmdb_id=movie_data['id'],
                    defaults={
                        'title': movie_data.get('title', ''),
                        'overview': movie_data.get('overview', ''),
                        'poster_path': movie_data.get('poster_path', ''),
                        'backdrop_path': movie_data.get('backdrop_path', ''),
                        'release_date': movie_data.get('release_date') or None,
                        'vote_average': movie_data.get('vote_average', 0),
                        'vote_count': movie_data.get('vote_count', 0),
                        'genre_ids': movie_data.get('genre_ids', []),
                    }
                )
                movies.append(movie)
            
            return movies
        
        return []
    
    @classmethod
    def get_popular_movies(cls):
        return cls.fetch_movies('movie/popular')
    
    @classmethod
    def get_top_rated_movies(cls):
        return cls.fetch_movies('movie/top_rated')
    
    @classmethod
    def get_upcoming_movies(cls):
        return cls.fetch_movies('movie/upcoming')
    
    @classmethod
    def search_movies(cls, query):
        return cls.fetch_movies('search/movie', {'query': query})
    
    @classmethod
    def get_movie_details(cls, movie_id):
        """Fetch single movie details from TMDB"""
        url = f"{cls.BASE_URL}/movie/{movie_id}"
        response = requests.get(url, headers=cls.get_headers())
        
        if response.status_code == 200:
            movie_data = response.json()
            
            # Create or update movie in database
            movie, created = Movie.objects.get_or_create(
                tmdb_id=movie_data['id'],
                defaults={
                    'title': movie_data.get('title', ''),
                    'overview': movie_data.get('overview', ''),
                    'poster_path': movie_data.get('poster_path', ''),
                    'backdrop_path': movie_data.get('backdrop_path', ''),
                    'release_date': movie_data.get('release_date') or None,
                    'vote_average': movie_data.get('vote_average', 0),
                    'vote_count': movie_data.get('vote_count', 0),
                    'genre_ids': [g['id'] for g in movie_data.get('genres', [])],
                }
            )
            
            return movie
        
        return None
