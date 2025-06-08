# orders/urls.py
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.orders_view, name='orders'),
    path('create/', views.create_order, name='create_order'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
]
