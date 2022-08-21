from core.settings.__init__ import *
import os
import dj_database_url

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = [os.environ.get('PRODUCTION_HOST')]

INSTALLED_APPS.extend(['whitenoise.runserver_nostatic'])

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

TEMPLATES[0]["DIRS"] = [os.path.join(BASE_DIR, '../', 'frontend', 'build')]

STATICFILES_DIRS = [os.path.join(
    BASE_DIR, '../', 'frontend', 'build', 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'
WHITENOISE_ROOT = os.path.join(BASE_DIR, '../', 'frontend', 'build', 'root')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASE_URL = os.environ.get('DATABASE_URL')
# db_from_env = dj_database_url.config(default=DATABASE_URL, conn_max_age=500, ssl_require=True)
# DATABASES['default'].update(db_from_env)

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_IMPORTS = ['services.tasks']
CELERY_RESULT_BACKEND = "django-db"