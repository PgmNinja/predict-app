from core.settings.__init__ import *
import environ

env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": env("SQL_DATABASE"),
        "USER": env("SQL_USER"),
        "PASSWORD": env("SQL_PASSWORD"),
        "HOST": env("SQL_HOST"),
        "PORT": env("SQL_PORT"),
    }
}
