import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

PARLER_DEFAULT_LANGUAGE_CODE = 'en'
PREFIX_DEFAULT_LANGUAGE = False

LANGUAGES = (
    ('en','English'),
    ('pl', 'Polish'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'portfolio/locale'),
    os.path.join(BASE_DIR, 'app_index/locale/'),
    os.path.join(BASE_DIR, 'app_owner/locale/'),
    os.path.join(BASE_DIR, 'app_projects/locale/'),
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
