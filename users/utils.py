import secrets
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

def send_verification_email(user, request):
    token = secrets.token_urlsafe(32)
    user.email_verification_token = token
    user.save()
    
    verification_url = request.build_absolute_uri(
        reverse('verify_email', args=[token])
    )
    
    send_mail(
        'Подтверждение email',
        f'Перейдите по ссылке для подтверждения: {verification_url}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

def send_password_reset_email(user, request):
    token = secrets.token_urlsafe(32)
    user.password_reset_token = token
    user.save()
    
    reset_url = request.build_absolute_uri(
        reverse('password_reset_confirm', args=[token])
    )
    
    send_mail(
        'Сброс пароля',
        f'Перейдите по ссылке для сброса пароля: {reset_url}',
        'noreply@bookshop.com',
        [user.email],
        fail_silently=False,
    )
