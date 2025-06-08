from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Установка кодировки для PostgreSQL
os.environ['PGCLIENTENCODING'] = 'UTF8'

# Секретный ключ и настройки безопасности
SECRET_KEY = 'django-insecure-(j2%(l@m2nb-xp)j(r1ah6y^lsl2af8p1n-bf5)62kc)aijl*b'
DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'products',
    'users',
    'cart',
    'orders',
    'payments'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.RBACMiddleware'
]

ROOT_URLCONF = 'bookshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bookshop.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bookshop',
        'USER': 'postgres',
        'PASSWORD': 'a21052011',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c client_encoding=utf8',
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SITE_ID = 1  # Укажите ID вашего сайта из админки
# Пользовательская модель
AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_REDIRECT_URL = '/'
# Настройки почты (пример для Gmail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'p0.student0s@gmail.com'
EMAIL_HOST_PASSWORD = 'ubnl wscy ggig arcu'
DEFAULT_FROM_EMAIL = 'p0.student0s@gmail.com'

# Куда перенаправлять после успешного входа
LOGIN_REDIRECT_URL = '/'
# Куда перенаправлять при необходимости войти
LOGIN_URL = '/login/'
# Куда перенаправлять при выходе из аккаунта
LOGOUT_REDIRECT_URL = '/'


LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True
MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
