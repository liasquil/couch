from base import *

# make tests faster
DEBUG = True
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = 'testkey9402t'
SOUTH_TESTS_MIGRATE = False

DATABASES = {
    'default': {'ENGINE': 'django.db.backends.sqlite3'}
}