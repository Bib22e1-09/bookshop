from django.contrib import admin
from .models import Book, Author, Genre, Publisher, Review

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    search_fields = ('full_name',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'price', 'stock', 'publisher', 'get_authors', 'get_genres', 'average_rating')
    list_filter = ('year', 'publisher', 'genres')
    search_fields = ('title', 'isbn')
    filter_horizontal = ('authors', 'genres')

    def get_authors(self, obj):
        return ", ".join([a.full_name for a in obj.authors.all()])
    get_authors.short_description = 'Авторы'

    def get_genres(self, obj):
        return ", ".join([g.name for g in obj.genres.all()])
    get_genres.short_description = 'Жанры'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
