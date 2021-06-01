"""
Django settings for portfolio project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

ALLOWED_HOSTS = ["127.0.0.1", 'rkaminski.herokuapp.com','rkam.dev']

CSRF_TRUSTED_ORIGINS = ["127.0.0.1", 'rkaminski.herokuapp.com','rkam.dev']
CSRF_COOKIE_DOMAIN = ".rkam.dev"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'

ROOT_URLCONF = 'portfolio.urls'

if not os.getenv('SECURE_SSL_REDIRECT') == 'False':
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

WSGI_APPLICATION = 'portfolio.wsgi.application'