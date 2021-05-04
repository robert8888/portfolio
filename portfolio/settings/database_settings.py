import os
import dj_database_url
from dotenv import load_dotenv
load_dotenv()

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = { 'default': {
    **dj_database_url.config(),
    **dj_database_url.config(os.getenv("DATABASE_URL"))
}}
