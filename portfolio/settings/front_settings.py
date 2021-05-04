import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

VUE_FRONTEND_DIR = os.path.join(BASE_DIR, 'components_src')

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not os.getenv('DEBUG') == 'True',
        'BUNDLE_DIR_NAME': 'vue/',  # must end with slash
        'STATS_FILE': os.path.join(VUE_FRONTEND_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map']
    }
}

SVG_DIRS=[
    os.path.join(BASE_DIR, 'assets', 'img')
]