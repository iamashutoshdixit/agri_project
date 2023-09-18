"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
from decouple import config
import boto3
from firebase_admin import initialize_app, credentials


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-#sc)=#&ov#2_0n_=j_f=8bv1xvrq8*9hk0h^&^qnanq=t-v)i="

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = DEBUG = os.environ.get("DEBUG", False)
DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = [
    "*",
]


# Application definition

DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework.authtoken",
    "rest_framework",
    "notifications",
    "push_notifications",
    "fcm_django",
]

USER_APPS = ["users", "farms", "pdc", "config", "labour", "accounts"]

INSTALLED_APPS = DEFAULT_APPS + USER_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "admin_reorder.middleware.ModelAdminReorder",
]

ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# WSGI_APPLICATION = "main.wsgi.application"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/info.log",
        },
        "error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/error.log",
        },
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["info", "error"],
        },
    },
}

AWS_ID = "AKIAXT3QGHQ76FCM5QVZ"
AWS_KEY = "WhBjY7wYkhzTISSwy3SliXIp0tKptrx69sKhnkh5"
AWS_REGION = config("AWS_REGION")
AWS_S3_BUCKET = config("AWS_S3_BUCKET")

if config("DEPLOYMENT") == "prod":
    AWS_ID = config("AWS_ID")
    AWS_KEY = config("AWS_KEY")

if config("DEPLOYMENT") == "prod_log":
    CLOUDWATCH_AWS_ID = config("AWS_ID")
    CLOUDWATCH_AWS_KEY = config("AWS_KEY")
    AWS_DEFAULT_REGION = config("AWS_REGION")
    boto3_logs_client = boto3.client(
        "logs",
        aws_access_key_id=CLOUDWATCH_AWS_ID,
        aws_secret_access_key=CLOUDWATCH_AWS_KEY,
        region_name=AWS_DEFAULT_REGION,
    )
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "aws": {
                "format": "%(asctime)s [%(levelname)-8s] %(message)s [%(pathname)s:%(lineno)d]",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["watchtower"],
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
            "watchtower": {
                "class": "watchtower.CloudWatchLogHandler",
                "boto3_client": boto3_logs_client,
                "log_group_name": "main",
                "level": "INFO",
            },
            "auth_file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": "/var/log/django/app/auth.log",
                "formatter": "default",
            },
        },
        "loggers": {
            "django": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
            "auth": {
                "level": "INFO",
                "handlers": ["auth_file"],
                "propagate": False,
            },
        },
    }

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("DATABASE_NAME"),
        "USER": config("DATABASE_USER"),
        "PASSWORD": config("DATABASE_PASSWORD"),
        "HOST": config("DATABASE_HOST"),
        "PORT": config("DATABASE_PORT", cast=int),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://" + config("CACHE_LOCATION"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "PAGE_SIZE": 20,
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = "users.User"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CELERY_TIMEZONE = "Asia/Kolkata"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

CSS_URL = "http://admin:admincss78234@3.110.2.32:8083"

PUSH_NOTIFICATIONS_SETTINGS = {
    "FCM_API_KEY": config("FCM_API_KEY"),
    # "GCM_API_KEY": "[your api key]",
    # "APNS_CERTIFICATE": "/path/to/your/certificate.pem",
    # "APNS_TOPIC": "com.example.push_test",
    # "WNS_PACKAGE_SECURITY_ID": "[your package security id, e.g: 'ms-app://e-3-4-6234...']",
    # "WNS_SECRET_KEY": "[your app secret key, e.g.: 'KDiejnLKDUWodsjmewuSZkk']",
    # "WP_PRIVATE_KEY": "/path/to/your/private.pem",
    # "WP_CLAIMS": {"sub": "mailto: development@example.com"},
}

FCM_DJANGO_SETTINGS = {
    "UPDATE_ON_DUPLICATE_REG_ID": True,
}

USE_X_FORWARDED_HOST = True

# fcm
cred = credentials.Certificate(os.path.join(BASE_DIR, "./firebase_creds.json"))
FIREBASE_APP = initialize_app(cred)
