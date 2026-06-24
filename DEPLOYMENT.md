# Deployment Guide

## Local Development

1. **Setup**
```bash
setup.bat
```

2. **Configure .env**
Edit `.env` file with your credentials:
- BOT_TOKEN
- CLICK credentials
- PRIVATE_CHANNEL_ID

3. **Run Web Server**
```bash
run_web.bat
```

4. **Run Bot**
```bash
run_bot.bat
```

## Production (Supabase + VPS)

### 1. Database Setup (Supabase)

1. Create Supabase project
2. Get PostgreSQL connection string
3. Update `.env`:
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=db.xxx.supabase.co
DB_PORT=5432
```

### 2. VPS Setup

1. **Install Dependencies**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx supervisor
```

2. **Clone Project**
```bash
git clone your-repo.git
cd telegram_subscription
```

3. **Setup Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
cp .env.example .env
nano .env
```

5. **Run Migrations**
```bash
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

### 3. Supervisor Configuration

Create `/etc/supervisor/conf.d/telegram_bot.conf`:
```ini
[program:telegram_bot]
command=/home/user/telegram_subscription/venv/bin/python manage.py runbot
directory=/home/user/telegram_subscription
user=user
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/telegram_bot.log
```

Create `/etc/supervisor/conf.d/django_web.conf`:
```ini
[program:django_web]
command=/home/user/telegram_subscription/venv/bin/gunicorn config.wsgi:application --bind 0.0.0.0:8000
directory=/home/user/telegram_subscription
user=user
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/django_web.log
```

Reload supervisor:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start all
```

### 4. Nginx Configuration

Create `/etc/nginx/sites-available/telegram_subscription`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /home/user/telegram_subscription/staticfiles/;
    }

    location /media/ {
        alias /home/user/telegram_subscription/media/;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/telegram_subscription /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. SSL (Optional)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Monitoring

Check bot status:
```bash
sudo supervisorctl status telegram_bot
```

Check logs:
```bash
tail -f /var/log/telegram_bot.log
tail -f /var/log/django_web.log
```

Restart services:
```bash
sudo supervisorctl restart telegram_bot
sudo supervisorctl restart django_web
```

## Backup

Database backup:
```bash
pg_dump -h db.xxx.supabase.co -U postgres -d postgres > backup.sql
```

Restore:
```bash
psql -h db.xxx.supabase.co -U postgres -d postgres < backup.sql
```
