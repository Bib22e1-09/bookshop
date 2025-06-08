from django.db import models
from django.conf import settings
from django.db.models import Avg
from django.db.models.functions import Coalesce

class Author(models.Model):
    full_name = models.CharField(max_length=100)
    def __str__(self):
        return self.full_name
    class Meta:
        db_table = 'products_author'

class Genre(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'products_genre'

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField(blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'products_publisher'

class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    year = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    pages = models.IntegerField(null=True, blank=True)
    format = models.CharField(max_length=50, blank=True)
    cover_url = models.URLField(blank=True)
    fragment_url = models.URLField(blank=True)
    publisher = models.ForeignKey('Publisher', on_delete=models.SET_NULL, null=True, blank=True)
    authors = models.ManyToManyField('Author', blank=True)
    genres = models.ManyToManyField('Genre', blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name='Средний рейтинг')

    @property
    def average_rating(self):
        return self.reviews.aggregate(
            avg_rating=Coalesce(Avg('rating'), 0.0)
        )['avg_rating']
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'products_book'
        ordering = ['title']
    def get_cover_image(self):
        if self.cover_url:
            return self.cover_url
        return f"https://covers.openlibrary.org/b/isbn/{self.clean_isbn()}-L.jpg"
    def clean_isbn(self):
        return self.isbn.replace('-', '').replace(' ', '')
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'products_book'

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'products_review'
        ordering = ['-created_at']
