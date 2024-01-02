"""
Django settings for fjob project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

import sentry_sdk
from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', get_random_secret_key())
APP_DOMAIN = os.getenv("APP_DOMAIN", "http://localhost:8000")
WORKING_MODE = str(os.getenv("WORKING_MODE"))

if WORKING_MODE == "prod":
    DEBUG = False
    ALLOWED_HOSTS = ["*"]
else:
    DEBUG = True
    ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    # applications
    'users',
    'location',
    'offer',
    'favourite',
    'company',
    'payment',
    'support',

    # packages
    'rest_framework',
    'drf_yasg',
    'rest_framework_swagger',
    'django_filters',
    'social_django',
    'corsheaders',
    'rest_framework.authtoken',
    'storages'

]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'users.authentication.CustomJWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '5/second',
        'user': '15/second'
    }
}

# Authentication

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

REDIRECT_URLS = []
try:
    REDIRECT_URLS = os.getenv('REDIRECT_URLS').split(',')
except:
    pass

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
    'ACTIVATION_URL': 'activation/{uid}/{token}',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'TOKEN_MODEL': None,
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': REDIRECT_URLS
}

AUTH_COOKIE = 'access'
AUTH_COOKIE_MAX_AGE = 60 * 60 * 24
AUTH_COOKIE_SECURE = os.getenv('AUTH_COOKIE_SECURE', 'True') == 'True'
AUTH_COOKIE_HTTP_ONLY = True
AUTH_COOKIE_PATH = '/'
AUTH_COOKIE_SAMESITE = 'None'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_AUTH_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_AUTH_SECRET_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['first_name', 'last_name']
SOCIAL_AUTH_FACEBOOK_KEY = os.getenv('FACEBOOK_AUTH_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.getenv('FACEBOOK_AUTH_SECRET_KEY')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'email, first_name, last_name'
}

CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000", "https://main.d3cjvuwb5x6i3c.amplifyapp.com"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ["https://main.d3cjvuwb5x6i3c.amplifyapp.com", ]
CSRF_TRUSTED_ORIGINS = ["https://kwlodarczyk.pro"]

# STRIPE
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
PRICE_BASIC = os.getenv("STRIPE_BASIC")
PRICE_STANDARD = os.getenv("STRIPE_STANDARD")
PRICE_ADVANCED = os.getenv("STRIPE_ADVANCED")

# GMAIL
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD_HOST_USER")

# Celery
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fjob.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'fjob.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
if WORKING_MODE == "dev":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "fjob",
            "USER": "fjob",
            "PASSWORD": "fjob123",
            "HOST": "db",
            "PORT": "5432",
        }
    }
elif WORKING_MODE == "prod":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv("GC_SQL_NAME"),
            'USER': os.getenv("GC_SQL_USER"),
            'PASSWORD': os.getenv("GC_SQL_PASSWORD"),
            'HOST': os.getenv("GC_SQL_HOST"),
        }
    }
elif WORKING_MODE == "test":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# AWS S3
if WORKING_MODE == "prod":
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", None)
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", None)
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", None)
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", None)
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_S3_VERIFY = True

    # Static files
    AWS_LOCATION = "static"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    # Public media files
    PUBLIC_MEDIA_LOCATION = "media"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"
    DEFAULT_FILE_STORAGE = 'fjob.storage_backend.PublicMediaStorage'

else:
    STATIC_URL = '/static/'
    STATIC_ROOT = 'static/'

    MEDIA_URL = "media/"
    MEDIA_ROOT = "media/"



ALLOWED_IMAGE_FORMATS = ['png', 'jpg', 'jpeg']
MAX_IMAGE_SIZE = (5 * 1024 * 1024)


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.UserAccount'

# Sentry
if WORKING_MODE == "prod":
    sentry_sdk.init(
        dsn=str(os.getenv("SENTRY")),
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
