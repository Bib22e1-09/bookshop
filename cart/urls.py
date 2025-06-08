# cart/urls.py
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('increment/<int:pk>/', views.increment_cart, name='increment_cart'),
    path('decrement/<int:pk>/', views.decrement_cart, name='decrement_cart'),
    path('process_payment/', views.process_payment, name='process_payment'),
]

