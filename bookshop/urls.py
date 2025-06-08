from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('books/', include('products.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('register/', user_views.register_view, name='register'),
    path('password-reset/<str:token>/', user_views.password_reset_confirm, name='password_reset_confirm'),
    path('payments/', include('payments.urls', namespace='payments')),
    path('verify-email/<str:token>/', user_views.verify_email, name='verify_email'),
]
