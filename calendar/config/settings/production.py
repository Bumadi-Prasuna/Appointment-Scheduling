from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = 'env("DJANGO_SECRET_KEY")'
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['mitrarobot.com', '15.207.106.213'])
ALLOWED_HOSTS = ['mitrarobot.com', '15.207.106.213', '127.0.0.1']
ALLOWED_HOSTS = ['*']

# DATABASES
DATABASES = {

    'default': {
        'HOST': 'localhost',
        'ATOMIC_REQUESTS': True,
        'PORT': '5432',
        'NAME': 'project',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'PASSWORD': 'password',
        'USER': 'project',
    },
}
# ------------------------------------------------------------------------------

# CACHES
# ------------------------------------------------------------------------------

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
#SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
#SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    'DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)
SECURE_BROWSER_XSS_FILTER = True
# SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
# SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
SECURE_SSL_REDIRECT = False
# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

# STORAGES
# ------------------------------------------------------------------------------
# https://django-storages.readthedocs.io/en/latest/#installation

