from .settings import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'medis2',
        'USER': 'postgres',
        'PASSWORD': 'VzQq83itlPhUH1Pyxvij',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
