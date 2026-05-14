Render deployment checklist and environment variables

This file lists recommended environment variables and notes to deploy the backend to Render (and the frontend repo). Adjust values for your project/service names.

Backend (Django) - required env vars
- DJANGO_SECRET_KEY: a secure random string
- DEBUG: false
- DATABASE_URL: PostgreSQL connection url (e.g. postgres://user:pass@host:5432/dbname)
	- (Supabase) You can use the Supabase DB connection string as `DATABASE_URL`.
		Example from Supabase: `postgres://postgres:<password>@db.<project>.supabase.co:5432/postgres`.
		Ensure `sslmode=require` is included in the URL or allow the Django adapter to require SSL.
- ALLOWED_HOSTS: comma-separated hostnames (e.g. example.onrender.com)
- CORS_ALLOWED_ORIGINS: comma-separated frontend URL(s) (e.g. https://your-frontend.onrender.com)
- DEFAULT_FROM_EMAIL: email used for outgoing mail (optional)

If using object storage for media/static (recommended):
- DEFAULT_FILE_STORAGE: e.g. storages.backends.s3boto3.S3Boto3Storage
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_STORAGE_BUCKET_NAME
- AWS_S3_REGION_NAME (optional)

Render-specific notes
- Use a Postgres managed service on Render and set `DATABASE_URL` from the service.
- For static files, either use S3-compatible storage or configure a Render persistent disk and set MEDIA_ROOT accordingly.
 - Alternatively, use Supabase as the Postgres provider: set `DATABASE_URL` to the Supabase connection string.
 - Supabase also provides object storage; to use it for `MEDIA` you can configure `django-storages`
	 with the S3-compatible endpoint and credentials (see Supabase Storage docs).
- Run `python manage.py migrate` as a deploy/ start command step, and `python manage.py collectstatic --noinput` if you serve static files.
- Set `gunicorn` or `uvicorn` as the web start command (e.g. `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`).

Frontend (Next.js) - required env vars (in Render or in repo as secrets for build)
- NEXT_PUBLIC_API_URL: https://<your-backend>.onrender.com
- NEXT_PUBLIC_BACKEND_URL: same as above (optional)
- NEXTAUTH_URL: https://<your-frontend>.onrender.com
- NEXTAUTH_SECRET: secure random string used by NextAuth

Quick deploy steps (recommended)
1. Push repositories to GitHub (git-to-Render).
2. Create Postgres service on Render; attach to backend service and copy `DATABASE_URL`.
3. Create backend web service in Render. Add env vars listed above.
4. Configure build and start commands: `pip install -r requirements/base.txt` (or use a runtime), `python manage.py migrate`, and start with `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`.
5. Create frontend web service on Render; set `NEXT_PUBLIC_API_URL` and `NEXTAUTH_URL`.
6. Enable automatic deploys from GitHub.

If you want, I can create a `render.yaml` to automate the Render configuration — tell me if you'd like that.
