"""
Django settings for portfolio project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ['rkaminski.herokuapp.com', "127.0.0.1"]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webp_converter',

    'storages',
    'webpack_loader',
    'solo.apps.SoloAppConfig',
    'fieldsets_with_inlines',
    'prettyjson',
    'imagefield',
    'compressor',
    'django.contrib.admin',
    'ckeditor',
    'ckeditor_uploader',
    'nested_admin',
    'polymorphic',
    'parler',

#     'projects.apps.ProjectsConfig',
    'app_index.apps.IndexAppConfig',
    'app_projects.apps.ProjectsAppConfig',
    'app_owner.apps.AppOwnerConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'portfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'portfolio/templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'webp_converter.context_processors.webp_support',
 #                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'portfolio.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = { 'default': {
    **dj_database_url.config(),
    **dj_database_url.config(os.getenv("DATABASE_URL"))
}}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

PARLER_DEFAULT_LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en','English'),
    ('pl', 'Polish'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

PARLER_LANGUAGES = {
    None: (
        {'code': 'en',},
        {'code': 'pl',},
    ),
    'default': {
        'fallbacks': ['en'],          # defaults to PARLER_DEFAULT_LANGUAGE_CODE
        'hide_untranslated': False,   # the default; let .active_translations() return fallbacks too.
    }
}
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'portfolio/locale'),
]

# prefix_default_language = False
# Static files (CSS, JavaScript, Images)


# AWS S3 SETTINGS
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_URL = os.getenv('AWS_URL')
AWS_DEFAULT_ACL = None
AWS_S3_REGION_NAME = 'eu-central-1'
AWS_S3_SIGNATURE_VERSION = 's3v4'


MEDIA_ROOT = AWS_URL + '/media/'
MEDIA_URL = AWS_URL + '/media/'
DEFAULT_FILE_STORAGE = 'portfolio.storage.MediaStorage'


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_compiled'),
    os.path.join(BASE_DIR, 'assets'),
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

COMPRESS_ENABLED = True
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]


# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'


VUE_FRONTEND_DIR = os.path.join(BASE_DIR, 'components_src')

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'vue/',  # must end with slash
        'STATS_FILE': os.path.join(VUE_FRONTEND_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map']
    }
}

CKEDITOR_UPLOAD_PATH = "upload"

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'prestige',
        'toolbar': 'Basic',
        'toolbar_Basic': [
            {'name': 'document', 'items': ['Templates', 'Source']},
            {'name': 'images', 'items': ['Image']},
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat', '-',
                       'PasteFromWord']},

            {'name': 'paragraph',
             'items': ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', 'NumberedList', 'BulletedList',
                       '-', 'Outdent', 'Indent', '-', 'Blockquote', '-',
                       ]},
            {'name': 'insert',
             'items': ['Table', 'HorizontalRule', 'SpecialChar', 'PageBreak']},

        ],
        'extraPlugins': ','.join(['sharedspace', 'save', 'autolink', ]),
        'removePlugins': ','.join(['resize', ]),
        'width': 'auto',
        'height': '4cm',
        'sharedSpaces': {
            'top': 'id-top-ckeditor-toolbar',
            'bottom': 'id-bottom-ckeditor-toolbar'
        },
        'contentsCss': '/static/front/css/ckeditor-content.css',
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'image2',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'templates',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath',
            'codemirror'
        ]),
        'codemirror': {
            'theme': 'lucario',
            'matchBrackets': True,
            'autoFormatOnStart': False,
            'mode': 'htmlmixed',
            'showTrailingSpace': False,
        },
        'allowedContent': True,
        'templates_files': ['/static/ckeditor/content_templates/editor-templates.js'],
    }
}