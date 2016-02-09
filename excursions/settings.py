"""
Django settings for excursions project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f8b1y=(i9e-+-2w)r3vr=f(x%ukka*y5buw2f+dxl_e7-2a-(y'

# initial credentials for admin account that will be created automatically:
# XXX: Do not forget to change this immediately via Django admin interface!
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'demodemo'

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
    'excursions',
    # 3rd party libs:
    'django_extensions',
    'debug_toolbar',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'excursions.urls'

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

WSGI_APPLICATION = 'excursions.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'excursions',
        'USER': 'eimantas',
        # 'PASSWORD': os.environ.get('PW', None),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

################
# API SETTINGS #
################

# DROPBOX_TOKEN = os.environ.get('DROPBOX_TOKEN', None)
DROPBOX_TOKEN = 'k1D1j_6mFuoAAAAAAAABPnh_RPlCjfI2TK_pmH9PAUR2iEIIDaGJgHX8ozDFikWp'

# path to the data files in Dropbox cloud. The files must be placed in the
# root directory for this app in Dropbox cloud ('/Dropbox/Apps/excursions/')
CITIES_REMOTE_DATA_FILE = '/city.csv'
HOTELS_REMOTE_DATA_FILE = '/hotel.csv'

# a location(directory name) in the server where remote files will be saved
# after periodical update:
LOCAL_DATA_LOCATION = os.path.join(BASE_DIR, 'data')

# A full path to the file that will be saved locally:
CITIES_LOCAL_DATA_FILE = os.path.join(
    LOCAL_DATA_LOCATION,
    # it's just file name with extension:
    os.path.basename(CITIES_REMOTE_DATA_FILE),
)
HOTELS_LOCAL_DATA_FILE = os.path.join(
    LOCAL_DATA_LOCATION,
    os.path.basename(HOTELS_REMOTE_DATA_FILE),
)
