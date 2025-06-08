from django.urls import path
from bookshop.views import home
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:pk>/review/', views.add_review, name='add_review'),
    path('create/', views.create_order, name='create_order'),
]
