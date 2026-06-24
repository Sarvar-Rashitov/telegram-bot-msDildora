from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu(is_registered=False):
    """Asosiy menyu - registratsiya holatiga qarab"""
    if is_registered:
        keyboard = [
            [KeyboardButton(text='👤 Profil'), KeyboardButton(text='💳 Obuna bo\'lish')],
            [KeyboardButton(text='📄 Litsenziya'), KeyboardButton(text='ℹ️ Ma\'lumot')],
            [KeyboardButton(text='📞 Yordam')],
        ]
    else:
        keyboard = [
            [KeyboardButton(text='📝 Ro\'yxatdan o\'tish')],
            [KeyboardButton(text='📄 Litsenziya'), KeyboardButton(text='ℹ️ Ma\'lumot')],
            [KeyboardButton(text='📞 Yordam')],
        ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def phone_request_keyboard():
    """Telefon raqam so'rash"""
    keyboard = [
        [KeyboardButton(text='📱 Telefon raqamni yuborish', request_contact=True)],
        [KeyboardButton(text='❌ Bekor qilish')],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)

def cancel_keyboard():
    """Bekor qilish tugmasi"""
    keyboard = [[KeyboardButton(text='❌ Bekor qilish')]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def tariff_menu(tariffs):
    keyboard = []
    for tariff in tariffs:
        keyboard.append([InlineKeyboardButton(
            text=f"{tariff.name} - {tariff.price} so'm",
            callback_data=f"tariff_{tariff.id}"
        )])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def payment_menu(payment_url):
    keyboard = [
        [InlineKeyboardButton(text='💳 To\'lov qilish', url=payment_url)],
        [InlineKeyboardButton(text='✅ To\'lovni tasdiqlash', callback_data='check_payment')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
