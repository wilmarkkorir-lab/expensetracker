from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    ".alwaysdata.net",
    "mysql-trackermoney.alwaysdata.net",
    "localhost",
    "127.0.0.1",
]

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "trackermoney_db",
        "USER": "trackermoney",
        "PASSWORD": "modcom2026",
        "HOST": "mysql-trackermoney.alwaysdata.net",
        "PORT": "3306",
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
