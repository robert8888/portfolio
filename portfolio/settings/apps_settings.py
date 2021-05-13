INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webp_converter',

    'app_cms_tpl.apps.CmsTplAppConfig',

    'storages',
    'webpack_loader',
    'solo.apps.SoloAppConfig',
    'fieldsets_with_inlines',
    'django_better_admin_arrayfield',
    'prettyjson',
    'imagefield',
    'puppeteer_pdf',
    'sortedm2m',
    'adminsortable2',
    'compressor',
    'admin_reorder',
    'django.contrib.admin',
    'ckeditor',
    'ckeditor_uploader',
    'nested_admin',
    'polymorphic',
    'rosetta',
    'parler',
    'svg',


    'app_cms.apps.CmsAppConfig',

    'app_projects.apps.ProjectsAppConfig',
    'app_owner.apps.AppOwnerConfig',

    'pwa',
]
