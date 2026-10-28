ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system app \
    && useradd --system --gid app --create-home --home-dir /home/app app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /app/docker/entrypoint.sh \
    && mkdir -p /app/staticfiles \
    && chown -R app:app /app

EXPOSE 8000

ENTRYPOINT ["/app/docker/entrypoint.sh"]

FROM base AS dev
USER root
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM base AS prod
USER app
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
