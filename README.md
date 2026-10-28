# Task Manager

Django task manager for IT teams: create tasks, assign workers, track deadlines,
organize work by teams and projects, and label tasks with tags.

## Stack

- Python 3.12
- Django 5
- PostgreSQL 16
- Gunicorn (production)
- Bootstrap 5
- Docker Compose profiles: `dev` / `prod`

## Domain model

- **Position** → many **Workers** (`Worker` extends `AbstractUser`)
- **Team** ↔ many **Workers**, owns many **Projects**
- **Project** → many **Tasks**
- **TaskType** → many **Tasks**
- **Task** ↔ many **assignees** (Workers), ↔ many **Tags**
- **Task.creator** → Worker who created the task

## Quick start (Docker)

```bash
cp .env.example .env
make up-dev
```

Open http://localhost:8000

Demo login after seed:

- username: `admin.user`
- password: `1qazcde3`

Useful commands:

```bash
make logs          # follow app logs
make migrate       # apply migrations
make seed          # reload demo data
make shell         # Django shell
make down          # stop containers
make up-prod       # production profile (Gunicorn)
make test          # local tests (SQLite)
make lint          # flake8
```

## Local development without Docker DB

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
export DJANGO_SETTINGS_MODULE=config.settings.test
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

For PostgreSQL locally, copy `.env.example` and point `POSTGRES_HOST` to your
database, then use `config.settings.dev`.

## Environment variables

See [`.env.example`](.env.example):

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Django secret (required in prod) |
| `ALLOWED_HOSTS` | Comma-separated hosts |
| `POSTGRES_*` | Database connection |
| `WEB_PORT` | Host port mapped to container `:8000` |
| `SEED_DEMO` | `1` to seed demo data on startup |

## Tests and lint

```bash
make test
make lint
```

Tests cover model relations, auth redirects, worker completed/incomplete split,
task create/assign/complete, and project/team pages.

## Project layout

```
config/           # Django project & settings (base/dev/prod/test)
tasks/            # App: models, views, forms, admin, seed command
templates/        # Bootstrap templates
static/css/       # Minimal styles
docker/           # Entrypoint
tests/            # Django TestCase suite
Dockerfile        # multi-stage: dev + prod
docker-compose.yml
Makefile
```

## Time zone

Application time zone is `Europe/Kyiv`.

## Security notes

- Task edit/delete/complete: creator, assignee, project-team member, or staff
- Team / tag / task-type management: staff only
- Project create/update: staff or member of the related team
- Production requires strong `SECRET_KEY` and `POSTGRES_PASSWORD`
- Demo credentials are shown on login only when `DEBUG=True`
- Postgres publish is bound to `127.0.0.1` only
- Login attempts are rate-limited per IP (10 / 5 minutes)
