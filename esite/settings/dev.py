from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c7$9grkpk#ykx4$9d9+)ndmldksuq_^4j)6_!i0svxesvc#n_2'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://localhost:8000'

try:
    from .local import *
except ImportError:
    pass
