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
DATABASES['default'] = dj_database_url.config(default='postgres://kjjittyukydluk:999c986e263f1b7892b0a969c1a09471c2c4f00b73641ebde9c898ec38bc8243@ec2-44-194-225-27.compute-1.amazonaws.com:5432/dffgnpd4653473')
