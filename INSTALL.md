# 📦 To'liq O'rnatish Ko'rsatmasi

## Tizim talablari

- Python 3.10+ 
- pip (Python package manager)
- Git
- Telegram Bot Token
- Click Payment hisob (ixtiyoriy)

## O'rnatish bosqichlari

### 1. Loyihani klonlash

```bash
git clone https://github.com/username/telegram-subscription.git
cd telegram-subscription
```

### 2. Virtual Environment

#### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux/Mac
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Dependencies o'rnatish

```bash
pip install -r requirements.txt
```

**Asosiy paketlar:**
- Django 5.0.6
- django-jazzmin 2.6.0 (Zamonaviy admin theme)
- aiogram 3.7.0 (Telegram bot)
- psycopg2-binary (PostgreSQL)
- python-decouple (Environment vars)
- Pillow (Image processing)
- requests
- APScheduler

### 4. Environment sozlamalari

`.env` fayl yarating:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

`.env` faylini tahrirlang:

```env
# Django
DEBUG=True
SECRET_KEY=your-random-secret-key-min-50-characters-long
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite default)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Yoki PostgreSQL
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=subscription_db
# DB_USER=postgres
# DB_PASSWORD=yourpassword
# DB_HOST=localhost
# DB_PORT=5432

# Telegram Bot (BotFather'dan oling)
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
BOT_USERNAME=YourBot

# Click Payment (https://my.click.uz)
CLICK_MERCHANT_ID=12345
CLICK_SERVICE_ID=67890
CLICK_SECRET_KEY=your_secret_key_here

# Private Channel (Bot admin bo'lishi kerak)
PRIVATE_CHANNEL_ID=-1001234567890
```

### 5. Database migratsiyalari

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Superuser yaratish

```bash
python manage.py createsuperuser
```

Kerakli ma'lumotlarni kiriting:
- Username: admin
- Email: admin@example.com
- Password: (xavfsiz parol)

### 7. Static fayllar

```bash
python manage.py collectstatic --noinput
```

## ✅ Ishga tushirish

### Development

**Terminal 1 - Web Server:**
```bash
python manage.py runserver
```

**Terminal 2 - Telegram Bot:**
```bash
python manage.py runbot
```

### URLs:
- Dashboard: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- Login: http://127.0.0.1:8000/login/

## 🔧 Qo'shimcha sozlamalar

### Telegram Bot sozlash

1. BotFather'da bot yarating: `/newbot`
2. Token oling va `.env` ga qo'shing
3. Bot username oling
4. Privacy mode o'chirib qo'ying (messages olish uchun)

### Private Channel yaratish

1. Telegram'da private channel yarating
2. Bot'ni kanalga admin qilib qo'shing
3. Channel ID oling:
   - Forward any message from channel to @userinfobot
   - Yoki bot orqali: channel'ga xabar yuboring va log'dan ID oling
4. `.env` ga qo'shing

### Click Payment sozlash

1. https://my.click.uz da ro'yxatdan o'ting
2. Merchant yarating
3. Service yarating
4. Credentials oling (.env ga)
5. Webhook URL sozlang:
   ```
   Prepare: https://yourdomain.com/payments/click/prepare/
   Complete: https://yourdomain.com/payments/click/complete/
   ```

### PostgreSQL o'rnatish (Production uchun)

#### Windows
1. PostgreSQL yuklab oling: https://www.postgresql.org/download/windows/
2. O'rnating
3. Database yarating:
```sql
CREATE DATABASE subscription_db;
CREATE USER dbuser WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE subscription_db TO dbuser;
```

#### Linux (Ubuntu)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo -u postgres createdb subscription_db
sudo -u postgres createuser dbuser
sudo -u postgres psql
ALTER USER dbuser WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE subscription_db TO dbuser;
\q
```

`.env` ni yangilang:
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=subscription_db
DB_USER=dbuser
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

Migratsiya qiling:
```bash
python manage.py migrate
```

## 🚀 Production Deployment

### 1. Sozlamalarni yangilash

```env
DEBUG=False
SECRET_KEY=<yangi-random-50+-chars>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### 2. Gunicorn o'rnatish

```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### 3. Nginx sozlash

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/project;
    }
    
    location /media/ {
        root /path/to/project;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. Systemd Service (Bot va Web)

**Web service** (`/etc/systemd/system/telegram-web.service`):
```ini
[Unit]
Description=Telegram Subscription Web
After=network.target

[Service]
User=youruser
WorkingDirectory=/path/to/project
ExecStart=/path/to/project/.venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Bot service** (`/etc/systemd/system/telegram-bot.service`):
```ini
[Unit]
Description=Telegram Subscription Bot
After=network.target

[Service]
User=youruser
WorkingDirectory=/path/to/project
ExecStart=/path/to/project/.venv/bin/python manage.py runbot
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable va start:
```bash
sudo systemctl enable telegram-web telegram-bot
sudo systemctl start telegram-web telegram-bot
sudo systemctl status telegram-web telegram-bot
```

### 5. SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## 🔍 Troubleshooting

### Bot ishlamayapti
```bash
# Token tekshirish
python manage.py shell
>>> from decouple import config
>>> print(config('BOT_TOKEN'))

# Log ko'rish
python manage.py runbot --log-level=DEBUG
```

### Migration xatosi
```bash
# Migration reset
python manage.py migrate --fake-initial
# Yoki
rm db.sqlite3
python manage.py migrate
```

### Static files topilmayapti
```bash
python manage.py collectstatic --clear
python manage.py collectstatic
```

### Permission denied (Linux)
```bash
chmod +x manage.py
sudo chown -R $USER:$USER .
```

## 📝 Keyingi qadamlar

1. ✅ Web dashboard'ga kiring
2. ✅ Tariflar yarating
3. ✅ Kanallar qo'shing
4. ✅ Bot'ni test qiling
5. ✅ To'lov tizimini test qiling

## 🆘 Yordam

- Documentation: [README.md](README.md)
- Quick Start: [QUICKSTART.md](QUICKSTART.md)
- Issues: GitHub Issues
- Telegram: @your_support

---

**Omad! 🎉**
