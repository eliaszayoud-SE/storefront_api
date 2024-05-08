from .common import *


DEBUG = True

SECRET_KEY = 'django-insecure-2_*jy$ocha@h45(cxa#cq4_w@7z+1x2fl=^tk$%i$g27=_rj8n'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}