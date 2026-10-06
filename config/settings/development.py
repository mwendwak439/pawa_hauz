"""
Development settings — used when running locally.
"""
from .base import *  # noqa

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Email backend: prints emails to console during development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Add debug toolbar here later if we choose to use it
INTERNAL_IPS = ['127.0.0.1']