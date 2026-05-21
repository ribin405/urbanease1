# C-URBANEASE

C-URBANEASE is a Django-based residential management web app with resident, admin, visitor, maintenance, and security portal workflows.

## Local Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

Update `.env` with a real `SECRET_KEY` before deploying.

## GitHub Checklist

- Do not commit `.env`, `venv/`, `db.sqlite3`, `staticfiles/`, or `__pycache__/`.
- Keep secrets in your hosting provider environment variables.
- Run `python manage.py check --deploy` before production deployment.

## Deployment Notes

Set these environment variables on your hosting platform:

```text
DJANGO_SECRET_KEY=<new-secret-key>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=<your-domain>,<your-app-host>
```

Before starting the app in production, run:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

The Django WSGI application is `config.wsgi:application`.
