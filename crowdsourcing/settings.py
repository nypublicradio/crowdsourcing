"""
Django settings for crowdsourcing project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import sys
import os
import posixpath
from distutils.util import strtobool

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
try:
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
except KeyError:
    from django.core.management.utils import get_random_secret_key
    SECRET_KEY = get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
try:
    DEBUG = strtobool(os.environ.get('DJANGO_DEBUG', 'False'))
except ValueError:
    DEBUG = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# These files do not follow Django's FORCE_SCRIPT_NAME directive.
DJANGO_URL_PREFIX = os.environ.get('DJANGO_URL_PREFIX')
STATIC_URL = posixpath.join(DJANGO_URL_PREFIX or '/', 'static/')

# Static files can be stored via S3 in demo/production.
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_QUERYSTRING_AUTH = False
AWS_LOCATION = DJANGO_URL_PREFIX
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')

if AWS_STORAGE_BUCKET_NAME and 'test' not in sys.argv:
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'surveys.apps.SurveysConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'raven.contrib.django.raven_compat',
    'rest_framework',
    'storages',
    'django_extensions',
    'adminsortable2',
    'corsheaders',
]

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

ROOT_URLCONF = 'crowdsourcing.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'crowdsourcing.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'postgres'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': int(os.environ.get('DB_PORT', 5432)),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Sentry
RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN')
}

CORS_ORIGIN_ALLOW_ALL = True

# Avoid conflicting with other django instances running on this domain
CSRF_COOKIE_PATH = '{}'.format(os.environ.get('DJANGO_URL_PREFIX') or '/')
SESSION_COOKIE_PATH = '{}'.format(os.environ.get('DJANGO_URL_PREFIX') or '/')
