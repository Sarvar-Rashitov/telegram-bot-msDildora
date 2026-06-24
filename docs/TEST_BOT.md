# 🧪 Bot Test Qo'llanma

## Muammo: Tugmalar ishlamayapti

### 1️⃣ Botni to'xtatish
Agar bot terminal'da ishlab turgan bo'lsa:
- `Ctrl + C` bosing
- Yoki terminalni yoping

### 2️⃣ Yangi terminal ochish
```bash
# Yangi terminal
cd C:\Users\Asus\Desktop\telegram-bot-msDildora
```

### 3️⃣ Virtual environment aktivlashtirish
```bash
.venv\Scripts\activate
```

### 4️⃣ Botni ishga tushirish
```bash
python manage.py runbot
```

## Debug Output

Botni ishga tushirganingizda quyidagi log'lar ko'rinadi:
```
INFO:__main__:Bot ishga tushmoqda...
INFO:__main__:Handler registratsiyasi:
INFO:__main__:- Message handlers: XX
INFO:__main__:- Callback handlers: 3
```

### Tugma bosilganda:

**Agar handler ishlasa:**
```
INFO:apps.bot.handlers.subscribe:Subscribe handler called by 123456789
INFO:apps.bot.handlers.subscribe:Subscribe message sent to 123456789
```

**Agar handler ishlamasa:**
```
WARNING:__main__:Unhandled message: '💳 Obuna bo'lish' from 123456789
```

## Tekshirish

### 1. Profile tugmasi
Telegram botda `👤 Profil` bosing
- ✅ Ishlasa: profil ma'lumotlari keladi
- ❌ Ishlamasa: "Debug: '👤 Profil' handler topilmadi"

### 2. Obuna bo'lish tugmasi  
Telegram botda `💳 Obuna bo'lish` bosing
- ✅ Ishlasa: tariflar ro'yxati keladi
- ❌ Ishlamasa: "Debug: '💳 Obuna bo\'lish' handler topilmadi"

## Agar hali ham ishlamasa

### 1. Cache muammosi
Bot eski fayllarni ishlayotgan bo'lishi mumkin.

**Yechim:**
```bash
# __pycache__ larni tozalash
rd /s /q apps\bot\__pycache__
rd /s /q apps\bot\handlers\__pycache__

# Qayta ishga tushirish
python manage.py runbot
```

### 2. State muammosi
FSM state stuck bo'lgan bo'lishi mumkin.

**Test:**
Botda `/start` bosing, keyin `💳 Obuna bo'lish` bosing

### 3. Tugma matni noto'g'ri
Keyboard va handler tekstlari mos emas bo'lishi mumkin.

**Tekshirish:**
```python
# Bot.py da:
F.text == '💳 Obuna bo\'lish'

# Keyboard.py da:
KeyboardButton(text='💳 Obuna bo\'lish')
```

## Quick Fix

Agar hech narsa ishlamasa, botni to'liq qayta boshlang:

```bash
# 1. Processni to'xtatish
taskkill /F /IM python.exe

# 2. Cache tozalash  
rd /s /q apps\bot\__pycache__

# 3. Qayta ishga tushirish
python manage.py runbot
```

## Log File

Log faylni yaratish:
```bash
python manage.py runbot > bot.log 2>&1
```

Keyin bot.log faylini ochib xatolarni ko'ring.
