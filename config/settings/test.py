"""Test settings (SQLite in-memory for speed)."""

from .base import *  # noqa: F401,F403

DEBUG = True

SECRET_KEY = "test-secret-key-not-for-production"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

MIDDLEWARE = [  # noqa: F405
    mw
    for mw in MIDDLEWARE  # noqa: F405
    if mw != "whitenoise.middleware.WhiteNoiseMiddleware"
]

STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
