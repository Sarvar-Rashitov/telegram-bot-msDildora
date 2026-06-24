# Render.com Deploy Qo'llanmasi

## Talab qiladigan ma'lumotlar

1. **PostgreSQL Database** (Supabase yoki AWS RDS)
   - Database URL
   - Username
   - Password
   - Host
   - Port (default: 5432)

2. **Django Environment Variables**
   - SECRET_KEY (strong random key)
   - BOT_TOKEN (Telegram bot token)
   - CLICK Payment credentials

## Deploy Qadamlari

### 1. GitHub-ga Push qiling
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Render.com-da Repo ulang
- https://render.com ga kiring
- New -> Web Service
- GitHub repository'ni tanlang
- Branch: main

### 3. Environment Variables o'rnatish

Render dashboard'da quyidagi variables o'rnatish:

```
DEBUG=False
SECRET_KEY=<strong-random-key>
ALLOWED_HOSTS=your-app.onrender.com

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=your-db-host.pooler.supabase.com
DB_PORT=5432

BOT_TOKEN=your-telegram-token
BOT_USERNAME=your-bot-username
CLICK_MERCHANT_ID=your-merchant-id
CLICK_SERVICE_ID=your-service-id
CLICK_SECRET_KEY=your-secret-key
```

### 4. Deploy

Deploy avtomatik boshlandi. Render logs'da status'ni kuzatish:

```
✓ Build started
✓ Dependencies installed
✓ Static files collected
✓ Database migrations applied
✓ Superuser created
✓ Server started on port 10000
```

### 5. Birinchi Login

Admin panel:
- URL: `https://your-app.onrender.com/admin`
- Username: `admin`
- Password: `admin123`

Web Dashboard:
- URL: `https://your-app.onrender.com/`

## Masalalar va Yechimlar

### "Build failed" Xatosi

Build qadamini tekshiring:
```
- runtime.txt da Python 3.11.9
- requirements.txt da barcha dependencies
- build.sh faylining permission'i executable
```

### Database Ulanish Xatosi

- PostgreSQL host'ni tekshiring
- Credentials to'g'ri kirganini tekshiring
- Firewall rules'ni tekshiring (Supabase)

### Static Files Ko'rinmayapti

Qo'lda static files collect qilish:
```bash
python manage.py collectstatic --noinput
```

## Backup va Maintenance

### Database Backup
Supabase dashboard'da:
1. Settings -> Backups
2. Automatic backups ON

### Logs Kuzatish
Render Dashboard -> Logs -> View Live Logs

### Updates Qilish

```bash
# Lokal o'zgarish
git add .
git commit -m "Update"
git push origin main

# Render avtomatik redeploy qiladi
```

## Security

- [ ] SECRET_KEY o'zgartirilgan
- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS to'g'ri
- [ ] HTTPS enabled (avtomatik)
- [ ] CSRF_COOKIE_SECURE = True

## Support

Masalalar uchun:
1. Render logs'ni tekshiring
2. Environment variables'ni verify qilingu
3. Database connection'ni test qilingu
