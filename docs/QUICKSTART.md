# ⚡ Tezkor Boshlash

5 daqiqada loyihani ishga tushiring!

## 1️⃣ O'rnatish (2 daqiqa)

```bash
# Virtual environment
python -m venv .venv
.venv\Scripts\activate

# Dependencies
pip install -r requirements.txt

# .env yaratish
copy .env.example .env
```

## 2️⃣ Sozlash (.env fayli) (1 daqiqa)

`.env` faylini oching va to'ldiring:

```env
# Asosiy
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production

# Bot (BotFather'dan oling)
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
BOT_USERNAME=your_bot

# Click (https://my.click.uz dan)
CLICK_MERCHANT_ID=12345
CLICK_SERVICE_ID=67890
CLICK_SECRET_KEY=your_secret

# Kanal ID (botni kanalga admin qiling va ID oling)
PRIVATE_CHANNEL_ID=-1001234567890
```

## 3️⃣ Database (1 daqiqa)

```bash
python manage.py migrate
python manage.py createsuperuser
```

Username, email, parol kiriting.

## 4️⃣ Ishga tushirish (1 daqiqa)

### Terminal 1 - Web Dashboard
```bash
python manage.py runserver
```

### Terminal 2 - Telegram Bot
```bash
python manage.py runbot
```

## ✅ Tayyor!

### Web Dashboard
🌐 http://127.0.0.1:8000/
- Login qiling (superuser)
- Dashboard'ni ko'ring

### Admin Panel
🔧 http://127.0.0.1:8000/admin/
- Jazzmin theme bilan chiroyli admin
- Barcha modellarni boshqaring

### Telegram Bot
💬 Telegram'da botingizni toping va `/start` bosing

---

## 🎯 Keyingi qadamlar

1. **Tarif yaratish** → `/subscriptions/tariffs/create/`
2. **Kanal qo'shish** → `/channels/create/`
3. **Test to'lov** → Telegram bot orqali

## ❓ Muammolar

### Bot ishlamayapti?
- `.env` da `BOT_TOKEN` to'g'ri ekanligini tekshiring
- `python manage.py runbot` ishlayotganligini tekshiring

### Login qila olmayapman?
- Superuser yaratdingizmi? `python manage.py createsuperuser`
- URL to'g'ri: `http://127.0.0.1:8000/login/`

### Click to'lov ishlamayapti?
- Click'dan test rejimida credentials oling
- Webhook URL sozlang: `https://yourdomain.com/payments/click/`

---

**🚀 Omad!**
