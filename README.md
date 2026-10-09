# VerdantSip

A full-stack e-commerce web app for an organic juice brand, built with Django 4.2.

## Features

- Product catalogue with search and allergen filtering
- Shopping cart and order management
- User authentication (register, login, password reset)
- Review system
- Admin panel for product and order management
- Email notifications on order placement

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2, SQLite |
| Frontend | Bootstrap 5, custom CSS |
| Auth | Django built-in auth |
| Forms | django-crispy-forms |
| Images | Pillow |

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Run migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DJANGO_SECRET_KEY` | Django secret key |
| `EMAIL_HOST_USER` | Gmail address for outgoing email |
| `EMAIL_HOST_PASSWORD` | Gmail app password |
| `EMAIL_RECEIVING_USER` | Address that receives order notifications |
