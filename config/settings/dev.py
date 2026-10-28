"""Development settings."""

import os

from .base import *  # noqa: F401,F403

DEBUG = True

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-dev-only-change-me-in-production",
)

ALLOWED_HOSTS = ["*"]

DATABASES["default"]["PASSWORD"] = os.environ.get(  # noqa: F405
    "POSTGRES_PASSWORD",
    "task_manager",
)
