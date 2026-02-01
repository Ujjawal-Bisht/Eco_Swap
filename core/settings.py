import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-64qmnwj83vdhk*x-@(k#5wx5@g=q%jd0*fg^l=r$u&9_8-qp*b'

# SECURITY WARNING: don't run with debug turned on in production!
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
    'rest_framework',
    'corsheaders',
    'users',      # Module 1
    'exchange',   # Module 2 & 4
    'centers',    # Module 3
    'community',  # Module 5
    'chat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # Correctly placed
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database configuration (MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecoswap_db',
        'USER': 'root',
        'PASSWORD': 'Dragoon', 
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# Auth Redirects (Add these for better flow)
LOGIN_REDIRECT_URL = 'item_list'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files (User uploaded content like item photos & success stories)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CORS setup for React/Frontend
CORS_ALLOW_ALL_ORIGINS = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Configuration for Password Reset
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Development mode - prints to console
# For production, use: 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-app-password'

# Password reset email settings
DEFAULT_FROM_EMAIL = 'noreply@ecoswap.com'
PASSWORD_RESET_TIMEOUT = 86400  # 24 hours in seconds


# 1. Static Files Configuration (Confirming paths)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
# STATIC_ROOT is used for production ('python manage.py collectstatic')
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 2. Media files (User uploaded content)
# Yeh URL browser mein images load karne ke liye use hoga
MEDIA_URL = '/media/'

# Yeh folder aapke local computer (IntelliJ project) par images save karega
MEDIA_ROOT = BASE_DIR / 'media'

# 3. Security Check for Media (Recommended for React/CORS)
# Agar aap frontend se image upload kar rahe hain, toh ye headers help karenge
CORS_ALLOW_ALL_ORIGINS = True