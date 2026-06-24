# 🚀 Telegram Premium Subscription Platform

Django + Aiogram 3 + Click Payment orqali professional Telegram obunalar platformasi.

## ✨ Asosiy Imkoniyatlar

### 🎯 Web Dashboard (Yangi!)
- **To'liq CRUD funksiyalar** - barcha ma'lumotlarni boshqarish
- **Real-time statistika** - jonli analitika va hisobotlar
- **Zamonaviy dizayn** - toza va intuitiv interfeys
- **Responsive** - barcha qurilmalarda ishlaydi

### 🤖 Telegram Bot
- Foydalanuvchilar ro'yxatdan o'tishi
- Obuna sotib olish
- Referal tizimi
- Ko'p tilli qo'llab-quvvatlash (O'zbek/Rus)

### 💳 To'lov tizimi
- Click payment integratsiyasi
- Avtomatik to'lovlarni qayta ishlash
- To'lovlar tarixi
- Promo kodlar

### 📊 Admin Panel
- **Django Jazzmin theme** - eng zamonaviy admin interfeys
- Barcha modellar uchun to'liq boshqaruv
- Qidirish va filtrlash
- Bulk actions

### 🎫 Qo'shimcha
- Support ticket tizimi
- Broadcast xabarlar yuborish
- Kanal boshqaruvi
- Audit log

## 📦 O'rnatish

### 1. Repository klonlash
```bash
git clone <repo-url>
cd telegram-subscription
```

### 2. Virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### 3. Dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt ichida:**
- Django 5.0.6
- django-jazzmin 2.6.0 ⭐ (Yangi admin theme)
- aiogram 3.7.0
- psycopg2-binary (PostgreSQL uchun)
- python-decouple
- Pillow (rasm ishlash)
- va boshqalar...

### 4. Environment sozlamalari
```bash
copy .env.example .env
```

`.env` faylini tahrirlang:
```env
DEBUG=True
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Telegram Bot
BOT_TOKEN=your_bot_token_from_botfather
BOT_USERNAME=your_bot_username

# Click Payment
CLICK_MERCHANT_ID=your_merchant_id
CLICK_SERVICE_ID=your_service_id
CLICK_SECRET_KEY=your_secret_key

# Channel
PRIVATE_CHANNEL_ID=-1001234567890
```

### 5. Database setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Superuser yaratish
```bash
python manage.py createsuperuser
```

### 7. Static fayllar
```bash
python manage.py collectstatic --noinput
```

## 🚀 Ishga tushirish

### Web Dashboard
```bash
python manage.py runserver
```
Dashboard: `http://127.0.0.1:8000/`
Login: yuqorida yaratgan superuser

### Telegram Bot
```bash
python manage.py runbot
```

## 📁 Loyiha tuzilishi

```
telegram-subscription/
├── apps/
│   ├── users/          # 👤 Foydalanuvchilar (CRUD ✅)
│   ├── subscriptions/  # 📅 Obunalar, tariflar (CRUD ✅)
│   ├── payments/       # 💰 To'lovlar (CRUD ✅)
│   ├── channels/       # 📢 Kanallar (CRUD ✅)
│   ├── broadcasts/     # 📨 Xabarlar (CRUD ✅)
│   ├── support/        # 💬 Support (CRUD ✅)
│   ├── analytics/      # 📊 Analitika
│   └── bot/            # 🤖 Telegram bot
├── templates/
│   ├── base.html       # Asosiy shablon
│   ├── dashboard/      # Dashboard sahifalar
│   ├── users/          # User sahifalar (list, detail, edit)
│   ├── subscriptions/  # Obuna sahifalar
│   └── ...
├── config/
│   ├── settings.py     # Django sozlamalari + Jazzmin config
│   └── urls.py
└── manage.py
```

## 🎨 Web Dashboard Sahifalar

### Dashboard (`/`)
- Umumiy statistika (users, subscriptions, revenue)
- So'nggi foydalanuvchilar
- So'nggi to'lovlar
- Tezkor havolalar

### Foydalanuvchilar (`/users/`)
- **List** - barcha foydalanuvchilar
- **Detail** - to'liq ma'lumot, obunalar tarixi
- **Edit** - tahrirlash (username, balance, status, va h.k.)
- **Delete** - o'chirish

### Obunalar (`/subscriptions/`)
- Obunalar ro'yxati
- **Tariflar** (`/subscriptions/tariffs/`)
  - Yaratish, tahrirlash, o'chirish
- **Promo kodlar** (`/subscriptions/promo/`)
  - Yaratish, o'chirish

### To'lovlar (`/payments/`)
- Barcha to'lovlar tarixi
- Status filtrlash

### Kanallar (`/channels/`)
- Yaratish, tahrirlash, o'chirish
- Member count ko'rish

### Broadcast (`/broadcasts/`)
- Yangi xabar yaratish
- Rasm yuklash
- Status tracking
- Detail sahifa

### Support (`/support/`)
- Ticket list
- Detail view
- Admin javob berish
- Status o'zgartirish

### Analitika (`/analytics/`)
- Real-time statistika
- Konversiya hisoblash
- Audit logs

## 🔧 Admin Panel

### URL
`http://127.0.0.1:8000/admin/`

### Jazzmin Theme Features
- ✅ Zamonaviy dizayn
- ✅ Responsive
- ✅ Custom icons (Font Awesome)
- ✅ Qidirish
- ✅ Filtrlash
- ✅ Export funksiyalari
- ✅ Dark mode (opsional)

### Admin'da boshqariladigan modellar:
- Users
- Tariffs
- Subscriptions
- Promo Codes
- Payments
- Channels
- Broadcasts
- Support Tickets
- Audit Logs

## 🔐 Xavfsizlik

- CSRF protection
- Login required decorators
- Admin permissions
- Secure password hashing
- Environment variables

## 📝 API Endpoints

### Click Payment
```
POST /payments/click/prepare/
POST /payments/click/complete/
```

## 🛠️ Development

### Yangi app qo'shish
```bash
python manage.py startapp app_name
```

### Migration yaratish
```bash
python manage.py makemigrations
python manage.py migrate
```

### Shell
```bash
python manage.py shell
```

## 📊 Database

Default: SQLite3 (development)
Production: PostgreSQL (tavsiya etiladi)

PostgreSQL sozlash:
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=subscription_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

## 🌐 Deployment

Production uchun:
1. `DEBUG=False` qiling
2. `ALLOWED_HOSTS` sozlang
3. `SECRET_KEY` o'zgartiring
4. PostgreSQL ishlatng
5. Gunicorn/Nginx sozlang
6. SSL sertifikat o'rnating

## 🤝 Contributing

1. Fork qiling
2. Feature branch yarating
3. Commit qiling
4. Push qiling
5. Pull request oching

## 📄 License

MIT License

## 👨‍💻 Muallif

Telegram: @your_username

## 🆘 Yordam

Muammo yuzaga kelsa:
1. Issues ochig
2. Dokumentatsiyani o'qing
3. Telegram orqali murojaat qiling

---

**⭐ Agar loyiha yoqsa, star bosishni unutmang!**
