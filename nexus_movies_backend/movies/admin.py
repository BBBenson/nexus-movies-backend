from django.contrib import admin
from .models import Movie, Favorite

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'tmdb_id', 'release_date', 'vote_average', 'created_at')
    list_filter = ('release_date', 'created_at')
    search_fields = ('title', 'tmdb_id')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'movie__title')
    ordering = ('-created_at',)
