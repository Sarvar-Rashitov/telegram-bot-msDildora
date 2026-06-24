# Production Deployment Checklist

## Pre-Deployment

- [ ] All migrations applied: `python manage.py migrate`
- [ ] Static files collected: `python manage.py collectstatic --noinput`
- [ ] Tests pass: `python manage.py test`
- [ ] No DEBUG statements in code
- [ ] ALLOWED_HOSTS configured correctly
- [ ] SECRET_KEY is strong and random
- [ ] Database backups enabled

## Django Settings

- [ ] DEBUG = False
- [ ] SECURE_SSL_REDIRECT = True
- [ ] SESSION_COOKIE_SECURE = True
- [ ] CSRF_COOKIE_SECURE = True
- [ ] SECURE_BROWSER_XSS_FILTER = True
- [ ] SECURE_CONTENT_SECURITY_POLICY configured

## Database

- [ ] PostgreSQL configured in settings.py
- [ ] Database host, user, password set
- [ ] Database port: 5432
- [ ] Connection pooling enabled (if available)

## Environment Variables

- [ ] SECRET_KEY set (strong, random string)
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS set to production domain
- [ ] DB_ENGINE=django.db.backends.postgresql
- [ ] DB_NAME, DB_USER, DB_PASSWORD set
- [ ] DB_HOST, DB_PORT configured
- [ ] BOT_TOKEN configured
- [ ] CLICK_* credentials configured

## Requirements

- [ ] requirements.txt updated
- [ ] python-decouple included
- [ ] gunicorn included
- [ ] whitenoise included
- [ ] psycopg2-binary included
- [ ] Pillow 11.0.0+ (for Python 3.14 compatibility)

## Build Configuration

- [ ] runtime.txt with Python 3.11.9
- [ ] Procfile with gunicorn command
- [ ] build.sh executable and correct
- [ ] render.yaml configured

## Render.com Specific

- [ ] GitHub repo connected
- [ ] Environment variables set in dashboard
- [ ] Auto-deploy on push enabled
- [ ] Health check configured
- [ ] Timeout settings appropriate

## After Deployment

- [ ] Health check passing
- [ ] Admin panel accessible
- [ ] Web dashboard working
- [ ] Database connected
- [ ] Static files served
- [ ] Error logs checked
- [ ] Superuser login tested

## Monitoring

- [ ] Render logs monitored
- [ ] Error notifications enabled
- [ ] Database metrics checked
- [ ] Server resources monitored

## Backup & Recovery

- [ ] Database backups enabled
- [ ] Backup retention period set
- [ ] Recovery procedure tested
- [ ] Document backup location

## Security Final Check

- [ ] No hardcoded passwords
- [ ] No DEBUG=True in production
- [ ] HTTPS enforced
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] CSRF protection enabled
- [ ] XSS protection enabled
- [ ] Security headers set
