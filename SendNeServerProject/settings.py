"""
Django settings for SendNeServerProject project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import posixpath
from os import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '76dd41a5-9f75-48e6-83c2-eb7e87d412f0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

####### Socket Server ############
#CHAT_WS_SERVER_HOST = 'localhost'
CHAT_WS_SERVER_HOST = '0.0.0.0'
#CHAT_WS_SERVER_PORT = 5002
CHAT_WS_SERVER_PORT = environ.get('PORT')
CHAT_WS_SERVER_PROTOCOL = 'ws'
#CHAT_WS_SERVER_PROTOCOL = 'https'


# Application definition

INSTALLED_APPS = [
    'app',
    'SendNeSocketsApp',

    # Add your apps here to enable them
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SendNeServerProject.urls'

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

WSGI_APPLICATION = 'SendNeServerProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''
import dj_database_url

#DATABASES['default'] =  dj_database_url.config(default=os.getenv('DATABASE_URL'))
'''
DATABASES = {
    'default': dj_database_url.config('DATABASE_URL')
}
'''

#DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'


#https://stackoverflow.com/questions/10228618/settings-databases-is-improperly-configured-error-performing-syncdb-with-djang
#postgres://user:pass@localhost/dbname
#HEROKU_POSTGRESQL_ONYX_URL: postgres://mkigesztkwaiqa:075d7a98e8c8b4fde6e9d9a5211dc31506c17689060c07ead092c0d3ce3ee251@ec2-50-17-203-51.compute-1.amazonaws.com:5432/d3trujo4q0vl5p
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your_heroku_db_name',
        'USER': 'your_heroku_db_user_name',
        'PASSWORD': 'your_heroku_password',
        'HOST': 'ec2-23-21-133-106.compute-1.amazonaws.com', # Or something like this
        'PORT': '5432',
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd3trujo4q0vl5p',
        'USER': 'mkigesztkwaiqa',
        'PASSWORD': '075d7a98e8c8b4fde6e9d9a5211dc31506c17689060c07ead092c0d3ce3ee251',
        'HOST': 'ec2-50-17-203-51.compute-1.amazonaws.com', # Or something like this
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

STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))

