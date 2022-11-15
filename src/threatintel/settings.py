import os
from pathlib import Path

from environs import Env
from configurations import Configuration


class BaseConfiguration(Configuration):

    # env
    env = Env()
    env.read_env("./.env")

    BASE_DIR = Path(__file__).resolve().parent.parent

    SECRET_KEY = env("SECRET_KEY", "etirgvonenrfnoerngorenogneongg334g")
    DEBUG = env.bool("DEBUG", True)

    ALLOWED_HOSTS = ["*", "0.0.0.0"]

    DJANGO_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",

    ]

    THIRD_PARTY_APPS = [
        "rest_framework",
        "django_filters",
        "django_apscheduler",
    ]

    LOCAL_APPS = [
        "src.intelhandler",
        "src.worker",
        "src.models"
    ]

    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "src.threatintel.urls"

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

    REST_FRAMEWORK = {
        'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 100
    }

    WSGI_APPLICATION = "src.threatintel.wsgi.application"

    DATABASES = {
        "default": {
            "ENGINE": env("POSTGRES_ENGINE", "django.db.backends.sqlite3"),
            "NAME": env("POSTGRES_DB", os.path.join(BASE_DIR, "db.sqlite3")),
            "USER": env("POSTGRES_USER", "user"),
            "PASSWORD": env("POSTGRES_PASSWORD", "password"),
            "HOST": env("POSTGRES_SERVER", "localhost"),
            "PORT": env("POSTGRES_DB_PORT", "5432"),
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

    LANGUAGE_CODE = "ru-RU"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_TZ = True

    STATIC_URL = "/static/"

    STATICFILES_DIRS = (str(BASE_DIR.joinpath("static_files")),)
    STATIC_ROOT = os.getenv("STATIC_ROOT", os.path.join(BASE_DIR, "static"))

    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    MEDIA_URL = "/media/"

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    KAFKA_GROUP_ID = env("KAFKA_GROUP_ID", "")
    KAFKA_TOPIC = env("KAFKA_TOPIC", "")
    KAFKA_IP = env("KAFKA_IP", "")
    AUTH_USER_MODEL = 'intelhandler.User'

    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
