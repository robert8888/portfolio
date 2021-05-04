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