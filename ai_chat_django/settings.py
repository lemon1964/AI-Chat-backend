# ai_chat_django/settings.py
from pathlib import Path
from decouple import config, Csv
from datetime import timedelta
import cloudinary

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("DJANGO_SECRET_KEY")
DJANGO_ENV = config("DJANGO_ENV", default="local")

if DJANGO_ENV == "local":
    DEBUG = config("DEBUG", default=True, cast=bool)
    ALLOWED_HOSTS = [
        "127.0.0.1",  # Локальный хост для тестов
        "localhost",  # Чтобы поддерживать локальный доступ через localhost
        "1256-178-128-39-136.ngrok-free.app",  # ngrok URL для публичных запросов
        "chatlemon64abc.pagekite.me",  # URL pagekite
        "591c3a8f9fea3e5451496639729483a5.serveo.net",  # URL serveo
    ]
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:3000",
        "https://1256-178-128-39-136.ngrok-free.app",
        "https://chatlemon64abc.pagekite.me",
        "https://591c3a8f9fea3e5451496639729483a5.serveo.net",
    ]
    CORS_ALLOW_ALL_ORIGINS = True
    CSRF_COOKIE_SECURE = False
    CSRF_COOKIE_HTTPONLY = False
    FRONT_URL = "http://localhost:3000"
    DOMAIN = "localhost:8000"
else:
    DEBUG = False
    ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
    CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", cast=Csv())
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    # продакт
    FRONT_URL = 'https://ai-chat-frontend-wy6h.onrender.com'
    DOMAIN = 'ai-chat-backend-3cba.onrender.com'

INSTALLED_APPS = [
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "dj_rest_auth",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "dj_rest_auth.registration",
    "corsheaders",
    "auth_app",
    "chat_app",
    "payment",
    "mermind",
]

AUTH_USER_MODEL = "auth_app.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "ai_chat_django.urls"

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

WSGI_APPLICATION = "ai_chat_django.wsgi.application"

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
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}


# Настройки аутентификации через email
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True  # Требуем email при регистрации
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # Требуем верификацию email
ACCOUNT_AUTHENTICATED_REDIRECT_URL = "/"  # Переадресация после успешной аутентификации

# Настройка для dj_rest_auth
REST_USE_JWT = True  # Используем JWT для аутентификации

SIMPLE_JWT = {
    # "ACCESS_TOKEN_LIFETIME": timedelta(minutes=100),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # По умолчанию
    "allauth.account.auth_backends.AuthenticationBackend",  # allauth
]

CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-csrftoken",
    "x-requested-with",
    "Cache-Control",
]

cloudinary.config(
    cloud_name=config("CLOUDINARY_CLOUD_NAME"),
    api_key=config("CLOUDINARY_API_KEY"),
    api_secret=config("CLOUDINARY_API_SECRET"),
    secure=True,
)

# Настройки для ЮKассы
SHOP_ID = config("SHOP_ID")
KASSA_SECRET_KEY = config("KASSA_SECRET_KEY")

# Импорт и настройка ЮKассы только после всех конфигураций
try:
    from yookassa import Configuration

    Configuration.configure(SHOP_ID, KASSA_SECRET_KEY)
except ImportError:
    print("Yookassa not installed")
except Exception as e:
    print(f"Error configuring Yookassa: {e}")


CRON_SECRET = config("CRON_SECRET", default="")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO",},
        "django.request": {"handlers": ["console"], "level": "WARNING"},
        "rest_framework.authentication": {"handlers": ["console"], "level": "INFO"},
        "payment": {"handlers": ["console"], "level": "INFO"},
        "auth_app": {"handlers": ["console"], "level": "INFO"},
        "mermind": {"handlers": ["console"], "level": "INFO"},
    },
}
