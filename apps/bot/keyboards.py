from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    keyboard = [
        [KeyboardButton(text='👤 Profil'), KeyboardButton(text='💳 Obuna bo\'lish')],
        [KeyboardButton(text='📞 Yordam'), KeyboardButton(text='ℹ️ Ma\'lumot')],
    ]
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
