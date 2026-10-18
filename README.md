# 💰 Paisa Tracker (Django)
Monthly money manager: income, kharcha, udhaar, saving, history, budget, CSV export.

## Features
- Har mahine ka report + pichle mahine ka balance auto carry-forward
- Income (e.g. 20k salary), Expense (category-wise), Kisi ne diya (Received), Udhaar diya / wapas mila, Saving
- Balance auto maintain; "udhaar baaki" list (kisse kitna lena hai)
- Monthly budget + progress bar, category breakdown
- Full history with filters (type/person/category/date) + CSV download
- Multi-user login, har user ka data alag

## Run locally
    python -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
Open http://127.0.0.1:8000 -> Register -> Add entries.

## Deploy (Render, free)
1. Push repo to GitHub.
2. Render -> New -> Blueprint -> select repo (uses `render.yaml`).
3. Production ke liye Render Postgres bana ke `DATABASE_URL` env set karo (warna SQLite reset ho sakta hai).

Env vars: SECRET_KEY, DEBUG=0, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, DATABASE_URL.
