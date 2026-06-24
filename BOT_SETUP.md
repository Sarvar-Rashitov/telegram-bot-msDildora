# 🤖 Bot Yangi Funksiyalar - Test Qo'llanma

## ✅ O'rnatilgan Yangi Funksiyalar

### 1. User Modeli Yangilandi
- `telegram_username` - Telegram username
- `age` - Yosh
- `occupation` - Kasb
- `is_registered` - To'liq ro'yxatdan o'tgan holat

### 2. Bot Models (Yangi)
- `BotSettings` - Bot sozlamalari (license fayl)
- `ContactInfo` - Yordam kontaktlari
- `BotInfo` - Bot haqida ma'lumotlar

### 3. Bot Handler-lari
- **Registration Flow** - To'liq ro'yxatdan o'tish (FSM)
- **License** - PDF fayl yuborish
- **Info** - Bot haqida ma'lumotlar
- **Help** - Yordam kontaktlari

### 4. Dashboard
- Bot sozlamalari CRUD
- Kontaktlar CRUD
- Ma'lumotlar CRUD

## 🚀 Ishga Tushirish

### 1. Migration
```bash
python manage.py migrate
```

### 2. Bot Sozlamalarini Yaratish
```bash
python manage.py init_bot_settings
```

### 3. Superuser bilan Dashboard'ga kirish
```bash
http://127.0.0.1:8000/admin/
```

### 4. Bot Settings sozlash
```bash
http://127.0.0.1:8000/bot/settings/
```

**Qo'shish kerak:**
1. License PDF faylini yuklash (BotSettings)
2. Yordam kontaktlarini qo'shish (ContactInfo)
3. Bot haqida ma'lumotlar qo'shish (BotInfo)

### 5. Botni ishga tushirish
```bash
python manage.py runbot
```

## 🎯 Bot Testlash

### Start - Yangi User
1. Botda `/start` bosing
2. Telegram ma'lumotlari avtomatik saqlanadi
3. "📝 Ro'yxatdan o'tish" tugmasi ko'rinadi

### Registration Flow
1. "📝 Ro'yxatdan o'tish" bosing
2. Ism kiriting
3. Familiya kiriting
4. Telefon raqam yuboring (tugma yoki matn)
5. Yosh kiriting
6. Kasb kiriting
7. ✅ Ro'yxatdan o'tish tugaydi

### License
1. "📄 Litsenziya" bosing
2. PDF fayl yuklanadi (admin panelda sozlangan bo'lsa)

### Ma'lumot
1. "ℹ️ Ma'lumot" bosing
2. Barcha faol ma'lumotlar ko'rinadi

### Yordam
1. "📞 Yordam" bosing
2. Barcha kontaktlar ko'rinadi

### Profil
1. "👤 Profil" bosing
2. To'liq ma'lumotlar ko'rinadi:
   - Ro'yxatdan o'tgan ✅/❌
   - Shaxsiy ma'lumotlar
   - Obuna holati

## 📊 Dashboard Testlash

### Users Ro'yxati
```
http://127.0.0.1:8000/users/
```
- Start bosgan userlar
- Registered userlar
- Filter: is_registered

### Bot Settings
```
http://127.0.0.1:8000/bot/settings/
```
- License PDF yuklash
- Kontaktlar qo'shish/tahrirlash
- Ma'lumotlar qo'shish/tahrirlash

### Admin Panel
```
http://127.0.0.1:8000/admin/
```
- User modelida yangi fieldlar
- BotSettings modeli
- ContactInfo modeli
- BotInfo modeli

## 🔍 Database Ko'rish

### Registered vs Non-Registered
```python
from apps.users.models import User

# Start bosgan
start_users = User.objects.filter(is_registered=False)

# To'liq ro'yxatdan o'tgan
registered_users = User.objects.filter(is_registered=True)
```

## 📝 Qo'shimcha

### Click Webhook URL-lar
`.env.example` da ko'rsatilgan:
- `CLICK_PREPARE_URL`
- `CLICK_COMPLETE_URL`
- `BOT_WEBHOOK_URL`

### FSM States
Bot `RegistrationStates` ishlatadi:
- waiting_for_first_name
- waiting_for_last_name
- waiting_for_phone
- waiting_for_age
- waiting_for_occupation

## ⚠️ Xatoliklar

Agar "SynchronousOnlyOperation" xatosi bo'lsa:
- Barcha handler-larda `@sync_to_async` decorator bor
- Barcha DB operatsiyalarda `close_old_connections()` chaqiriladi
- Middleware to'g'rilangan

## 🎉 Natija

Bot endi quyidagilarni qiladi:
1. ✅ Start bosgan userlarni saqlaydi
2. ✅ To'liq ro'yxatdan o'tish jarayoni
3. ✅ License PDF yuboradi
4. ✅ Ma'lumotlar ko'rsatadi
5. ✅ Yordam kontaktlarini ko'rsatadi
6. ✅ Dashboard orqali kontent boshqaruvi
