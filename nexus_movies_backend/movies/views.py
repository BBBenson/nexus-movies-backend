from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Movie, Favorite
from .serializers import MovieSerializer, FavoriteSerializer
from .services import TMDBService

@api_view(['GET'])
@permission_classes([AllowAny])
def get_movies(request):
    """Get movies by category"""
    category = request.GET.get('category', 'popular')
    
    try:
        if category == 'popular':
            movies = TMDBService.get_popular_movies()
        elif category == 'top_rated':
            movies = TMDBService.get_top_rated_movies()
        elif category == 'upcoming':
            movies = TMDBService.get_upcoming_movies()
        else:
            movies = TMDBService.get_popular_movies()
        
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def search_movies(request):
    """Search movies"""
    query = request.GET.get('q', '')
    
    if not query:
        return Response({'error': 'Query parameter is required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    try:
        movies = TMDBService.search_movies(query)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def get_movie_details(request, movie_id):
    """Get movie details by ID"""
    try:
        movie = TMDBService.get_movie_details(movie_id)
        if movie:
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'Movie not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def favorites(request):
    """Get user favorites or add a favorite"""
    if request.method == 'GET':
        user_favorites = Favorite.objects.filter(user=request.user)
        serializer = FavoriteSerializer(user_favorites, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        movie_id = request.data.get('movie_id')
        
        if not movie_id:
            return Response(
                {'error': 'movie_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Get or create movie from TMDB
            movie = TMDBService.get_movie_details(movie_id)
            if not movie:
                return Response(
                    {'error': 'Movie not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Create favorite
            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
                movie=movie
            )
            
            if created:
                serializer = FavoriteSerializer(favorite)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'message': 'Movie already in favorites'}, 
                    status=status.HTTP_200_OK
                )
        
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_favorite(request, movie_id):
    """Remove a movie from favorites"""
    try:
        movie = get_object_or_404(Movie, tmdb_id=movie_id)
        favorite = get_object_or_404(Favorite, user=request.user, movie=movie)
        favorite.delete()
        
        return Response(
            {'message': 'Movie removed from favorites'}, 
            status=status.HTTP_200_OK
        )
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
