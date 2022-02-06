from core.settings.__init__ import *
import os
import dj_database_url

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['epl-prediction-app.herokuapp.com', 'www.epl-prediction-app.herokuapp.com']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         "NAME": os.environ.get("SQL_DATABASE"),
#         "USER": os.environ.get("SQL_USER"),
#         "PASSWORD": os.environ.get("SQL_PASSWORD"),
#         "HOST": os.environ.get("SQL_HOST"),
#         "PORT": os.environ.get("SQL_PORT"),
#     }
# }
DATABASES = {}
DATABASES['default'] = dj_database_url.config(default='postgres://vqikhoufeoinjn:569c8d40ef73c60ca9c6a321ce6439b6edb20ca9e97284af920ad794b71a23cf@ec2-3-230-199-240.compute-1.amazonaws.com:5432/dfrtf4g287ef1j')
