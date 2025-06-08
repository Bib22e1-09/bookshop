from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import (
    CustomUserCreationForm,
    RegistrationForm,
    PasswordResetRequestForm,
    PasswordResetConfirmForm
)

from .utils import send_verification_email, send_password_reset_email

User = get_user_model()

def customer_check(user):
    return user.role == 'customer'

@user_passes_test(customer_check)
def customer_view(request):
    ...

def register_view(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_verification_email(user, request)
            messages.success(request, 'Письмо с подтверждением отправлено на ваш email.')
            return redirect('login')
        else:
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    """Авторизация пользователя"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            # Проверка подтверждения email
            if not user.email_verified:
                messages.error(request, 'Подтвердите email для входа.')
                return redirect('login')
            
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверные логин или пароль')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    """Выход из системы"""
    logout(request)
    return redirect('home')

def verify_email(request, token):
    """Подтверждение email по токену"""
    try:
        user = User.objects.get(email_verification_token=token)
        if user.email_verified:
            messages.info(request, 'Email уже подтверждён.')
            return redirect('login')
        user.email_verified = True
        user.email_verification_token = get_random_string(50)
        user.save()
        messages.success(request, 'Email успешно подтверждён! Теперь вы можете войти.')
        return redirect('login')
    except User.DoesNotExist:
        messages.error(request, 'Неверная или устаревшая ссылка подтверждения.')
        return redirect('login')

def password_reset_request(request):
    """Запрос на сброс пароля"""
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                send_password_reset_email(user, request)
                messages.success(request, 'Письмо с инструкциями отправлено на ваш email.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'Пользователь с таким email не найден.')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'users/password_reset_request.html', {'form': form})

def password_reset_confirm(request, token):
    """Подтверждение сброса пароля"""
    try:
        user = User.objects.get(password_reset_token=token)
        
        if request.method == 'POST':
            form = PasswordResetConfirmForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['new_password'])
                user.password_reset_token = get_random_string(50)
                user.save()
                messages.success(request, 'Пароль успешно изменён!')
                return redirect('login')
        else:
            form = PasswordResetConfirmForm()
            
        return render(request, 'users/password_reset_confirm.html', {'form': form})
        
    except User.DoesNotExist:
        messages.error(request, 'Неверная или устаревшая ссылка для сброса пароля.')
        return redirect('login')

class SignUpView(CreateView):
    """Регистрация через CBV"""
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
