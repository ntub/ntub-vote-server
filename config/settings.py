"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import environ

from split_settings.tools import include


env = environ.Env()
env.read_env()

root = environ.Path(__file__) - 2

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=False)
MODE = env('MODE', default='develop' if DEBUG else 'production')

include(
    'components/*.py',
    'environments/{}.py'.format(MODE),
)
