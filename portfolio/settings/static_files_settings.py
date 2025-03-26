import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# AWS S3 SETTINGS
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_URL = os.getenv('AWS_URL')
AWS_DEFAULT_ACL = None
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_S3_SIGNATURE_VERSION = 's3v4'

AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN')

AWS_S3_ADDRESSING_STYLE = "virtual"
AWS_QUERYSTRING_EXPIRE="518400"

MEDIA_ROOT_PATH = "media/"
MEDIA_ROOT = AWS_URL + MEDIA_ROOT_PATH
MEDIA_URL = AWS_URL + MEDIA_ROOT_PATH
DEFAULT_FILE_STORAGE = 'portfolio.storage.MediaStorage'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_compiled'),
    os.path.join(BASE_DIR, 'assets'),
]


def force_set_cache_header(headers, path, url):
    headers['Cache-Control'] = f'max-age={60 * 60 * 24 * 180}, public'

WHITENOISE_ADD_HEADERS_FUNCTION = force_set_cache_header

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

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
COMPRESS_STORAGE = 'portfolio.storage.AssetStorage'