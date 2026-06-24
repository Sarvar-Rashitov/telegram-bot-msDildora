# 🤖 Bot Muammolarini Hal Qilish

## ❌ SynchronousOnlyOperation xatosi

### Muammo:
```
django.core.exceptions.SynchronousOnlyOperation: You cannot call this from an async context
```

### Sabab:
Django ORM sync, Aiogram async. Django database operatsiyalarini async funksiyalarda to'g'ridan-to'g'ri ishlatib bo'lmaydi.

### ✅ Yechim:
Barcha Django ORM operatsiyalarini `sync_to_async` ga o'rang:

```python
from asgiref.sync import sync_to_async
from apps.users.models import User

@sync_to_async
def get_user(telegram_id):
    return User.objects.filter(telegram_id=telegram_id).first()

async def cmd_profile(message: Message):
    user = await get_user(message.from_user.id)
    # ...
```

### To'g'rilangan fayllar:
- ✅ `apps/bot/handlers/start.py`
- ✅ `apps/bot/handlers/profile.py`
- ✅ `apps/bot/handlers/subscribe.py`
- ✅ `apps/bot/handlers/support.py`
- ✅ `apps/bot/handlers/callbacks.py`

---

## 🔍 Bot javob bermayapti

### Tekshirish:

1. **Bot token to'g'rimi?**
```bash
# .env faylni oching
cat .env | grep BOT_TOKEN
```

2. **Bot ishga tushganmi?**
```bash
python manage.py runbot
```

Log'da ko'rishingiz kerak:
```
INFO:root:Bot ishga tushmoqda...
```

3. **Database migration qilinganmi?**
```bash
python manage.py migrate
```

4. **Telegram'da bot active mi?**
- BotFather'da botni toping
- `/mybots` → botingizni tanlang
- Bot aktiv ekanligini tekshiring

---

## ⚠️ Handlers ro'yxatdan o'tmagan

### Muammo:
```
INFO:aiogram.event:Update id=xxx is not handled
```

### Yechim:
Handler'lar `bot.py` da ro'yxatdan o'tganligini tekshiring:

```python
# apps/bot/bot.py
dp.message.register(start.cmd_start, Command('start'))
dp.message.register(profile.cmd_profile, F.text == '👤 Profil')
# ...
```

---

## 💾 Database xatosi

### Muammo:
```
django.db.utils.OperationalError: no such table
```

### Yechim:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🔐 Permission Denied

### Muammo:
Bot kanalga qo'sha olmayapti yoki xabar yubora olmayapti.

### Yechim:
1. Botni kanalga admin qilib qo'shing
2. Bot'ga kerakli huquqlar bering:
   - Post messages
   - Delete messages
   - Invite users via link

---

## 🌐 Click Payment ishlamayapti

### Tekshirish:

1. **Click credentials to'g'rimi?**
```bash
cat .env | grep CLICK
```

2. **Webhook URLs sozlanganmi?**
- Click.uz panelga kiring
- Service sozlamalariga kiring
- Webhook URLs ni tekshiring:
  ```
  Prepare: https://yourdomain.com/payments/click/prepare/
  Complete: https://yourdomain.com/payments/click/complete/
  ```

3. **Local testlash uchun:**
ngrok yoki localtunnel ishlatign:
```bash
ngrok http 8000
# URL: https://xxxx.ngrok.io/payments/click/prepare/
```

---

## 🐛 Debug rejimi

Bot'ni debug rejimida ishlatish:

```python
# apps/bot/bot.py
import logging

logging.basicConfig(level=logging.DEBUG)  # INFO → DEBUG
```

---

## 📋 Useful Commands

### Bot'ni qayta ishga tushirish:
```bash
# Windows
taskkill /F /IM python.exe
python manage.py runbot

# Linux
pkill -f "python manage.py runbot"
python manage.py runbot
```

### Log'larni ko'rish:
```bash
python manage.py runbot 2>&1 | tee bot.log
```

### Database'ni tozalash:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 🆘 Common Errors & Solutions

| Error | Sabab | Yechim |
|-------|-------|--------|
| `Token is invalid` | Bot token noto'g'ri | BotFather'dan yangi token oling |
| `Connection timeout` | Internet yo'q | Internetni tekshiring |
| `Module not found` | Paket o'rnatilmagan | `pip install -r requirements.txt` |
| `sync_to_async not found` | asgiref o'rnatilmagan | `pip install asgiref` |
| `No handlers registered` | Handler ro'yxatdan o'tmagan | `bot.py`ni tekshiring |

---

## ✅ Test Checklist

Bot ishga tushirishdan oldin:

- [ ] `.env` to'ldirildi
- [ ] `pip install -r requirements.txt` qilindi
- [ ] `python manage.py migrate` qilindi
- [ ] `python manage.py createsuperuser` qilindi
- [ ] Bot token to'g'ri
- [ ] Bot BotFather'da aktiv
- [ ] Kanal yaratildi va bot admin
- [ ] Channel ID `.env` ga qo'shildi

---

## 📞 Yordam

Muammo hal bo'lmasa:
1. Log'ni to'liq ko'ring
2. Error message'ni Google'ga qidiring
3. GitHub Issues'da izlang
4. Telegram orqali murojaat qiling

**Omad! 🚀**
