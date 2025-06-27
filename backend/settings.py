# backend/backend/settings.py
from pathlib import Path
from decouple import config, Csv
import cloudinary

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("DJANGO_SECRET_KEY")

# Определение окружения (local или production)
DJANGO_ENV = config('DJANGO_ENV')

if DJANGO_ENV == 'local':
    
    DEBUG = config('DEBUG', default=True, cast=bool)
    CSRF_COOKIE_SECURE = False
    CSRF_COOKIE_HTTPONLY = False
    
    # ALLOWED_HOSTS = ['*']
    ALLOWED_HOSTS = [
    '127.0.0.1',  # Локальный хост для тестов
    'localhost',  # Чтобы поддерживать локальный доступ через localhost
]
    CORS_ALLOW_ALL_ORIGINS = True
    
    FRONT_URL = "http://localhost:3000"
    DOMAIN = "localhost:8000"
    
else:
    DEBUG = False
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True

    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())
    CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='', cast=Csv())

    # заменить на продакт
    FRONT_URL = 'https://ai-chat-frontend-wy6h.onrender.com'
    DOMAIN = 'ai-chat-backend-3cba.onrender.com'
    
INSTALLED_APPS = [
    'django.contrib.sites',  # Обязательно для django-allauth
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "cloudinary",
    "cloudinary_storage",
    "django.contrib.staticfiles",
    'django_extensions',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    "allauth.socialaccount.providers.google",
    'dj_rest_auth.registration',
    'corsheaders',
    'auth_app',
    'chat_app',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'corsheaders.middleware.CorsMiddleware',  # Должен быть добавлен перед 'CommonMiddleware'
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'allauth.account.middleware.AccountMiddleware',  # Добавляем сюда

]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
          
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


AUTH_USER_MODEL = 'auth_app.User'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Настройка почтового сервера Для Gmail
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

# Настройки аутентификации через email
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True  # Требуем email при регистрации
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Требуем верификацию email
ACCOUNT_AUTHENTICATED_REDIRECT_URL = "/"  # Переадресация после успешной аутентификации

# Настройка для dj_rest_auth
REST_USE_JWT = True  # Используем JWT для аутентификации

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    # 'ACCESS_TOKEN_LIFETIME': timedelta(seconds=5.5),
    # 'REFRESH_TOKEN_LIFETIME': timedelta(seconds=20.5),
    # 'ACCESS_TOKEN_LIFETIME': timedelta(days=29),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}


SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # По умолчанию
    'allauth.account.auth_backends.AuthenticationBackend',  # allauth
]

CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-csrftoken",
    "x-requested-with",
    'Cache-Control',
]

REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "backend.auth_app.serializers.CustomRegisterSerializer",
    # В случае, если вы хотите использовать отдельный сериализатор для OAuth регистрации,
    # добавьте его сюда. Например, если у вас есть сериализатор для соцсетей:
    "OAUTH_REGISTER_SERIALIZER": "backend.auth_app.serializers.OAuthUserSerializer",
    "VERIFY_EMAIL": "path.to.CustomVerifyEmailView",
}

DJANGO_SETTINGS_MODULE = {
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}/',
}

cloudinary.config(
    cloud_name = config('CLOUDINARY_CLOUD_NAME'),
    api_key = config('CLOUDINARY_API_KEY'),
    api_secret = config('CLOUDINARY_API_SECRET'),
    secure=True
)

