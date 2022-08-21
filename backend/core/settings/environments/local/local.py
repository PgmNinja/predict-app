from core.settings.__init__ import *
import environ

env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ["backend", "localhost", "127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'epl-prediction-db',
        'USER': 'postgres',
        'PASSWORD': '@Niranjana99',
        'HOST': 'localhost',
        'PORT':'5432',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_IMPORTS = ['services.tasks']
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ALWAYS_EAGER = True

