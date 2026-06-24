from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from apps.users.models import User
from apps.bot.states import RegistrationStates
from apps.bot.keyboards import phone_request_keyboard, cancel_keyboard, main_menu
from django.db import close_old_connections

@sync_to_async
def check_user_registration(telegram_id):
    close_old_connections()
    user = User.objects.filter(telegram_id=telegram_id).first()
    return user, user.is_registered if user else False

@sync_to_async
def update_user_data(telegram_id, **kwargs):
    close_old_connections()
    User.objects.filter(telegram_id=telegram_id).update(**kwargs)
    user = User.objects.get(telegram_id=telegram_id)
    return user

async def cmd_register(message: Message, state: FSMContext):
    """Ro'yxatdan o'tish boshlash"""
    user, is_registered = await check_user_registration(message.from_user.id)
    
    if is_registered:
        await message.answer(
            "✅ Siz allaqachon ro'yxatdan o'tgansiz!",
            reply_markup=main_menu(True)
        )
        return
    
    await state.set_state(RegistrationStates.waiting_for_first_name)
    await message.answer(
        "📝 Ro'yxatdan o'tish\n\n"
        "Ismingizni kiriting:",
        reply_markup=cancel_keyboard()
    )

async def process_first_name(message: Message, state: FSMContext):
    """Ism qabul qilish"""
    if message.text == '❌ Bekor qilish':
        await state.clear()
        user, is_registered = await check_user_registration(message.from_user.id)
        await message.answer("❌ Bekor qilindi", reply_markup=main_menu(is_registered))
        return
    
    await state.update_data(first_name=message.text)
    await state.set_state(RegistrationStates.waiting_for_last_name)
    await message.answer(
        "Familiyangizni kiriting:",
        reply_markup=cancel_keyboard()
    )

async def process_last_name(message: Message, state: FSMContext):
    """Familiya qabul qilish"""
    if message.text == '❌ Bekor qilish':
        await state.clear()
        user, is_registered = await check_user_registration(message.from_user.id)
        await message.answer("❌ Bekor qilindi", reply_markup=main_menu(is_registered))
        return
    
    await state.update_data(last_name=message.text)
    await state.set_state(RegistrationStates.waiting_for_phone)
    await message.answer(
        "Telefon raqamingizni yuboring:\n"
        "(Tugmani bosing yoki +998XXXXXXXXX formatda kiriting)",
        reply_markup=phone_request_keyboard()
    )

async def process_phone(message: Message, state: FSMContext):
    """Telefon raqam qabul qilish"""
    if message.text == '❌ Bekor qilish':
        await state.clear()
        user, is_registered = await check_user_registration(message.from_user.id)
        await message.answer("❌ Bekor qilindi", reply_markup=main_menu(is_registered))
        return
    
    # Telefon raqam olish
    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text
    
    await state.update_data(phone=phone)
    await state.set_state(RegistrationStates.waiting_for_age)
    await message.answer(
        "Yoshingizni kiriting (raqamda):",
        reply_markup=cancel_keyboard()
    )

async def process_age(message: Message, state: FSMContext):
    """Yosh qabul qilish"""
    if message.text == '❌ Bekor qilish':
        await state.clear()
        user, is_registered = await check_user_registration(message.from_user.id)
        await message.answer("❌ Bekor qilindi", reply_markup=main_menu(is_registered))
        return
    
    if not message.text.isdigit():
        await message.answer("⚠️ Iltimos, faqat raqam kiriting!")
        return
    
    age = int(message.text)
    if age < 10 or age > 100:
        await message.answer("⚠️ Yoshni to'g'ri kiriting (10-100 oralig'ida)")
        return
    
    await state.update_data(age=age)
    await state.set_state(RegistrationStates.waiting_for_occupation)
    await message.answer(
        "Kasbingizni kiriting:",
        reply_markup=cancel_keyboard()
    )

async def process_occupation(message: Message, state: FSMContext):
    """Kasb qabul qilish va ro'yxatdan o'tishni yakunlash"""
    if message.text == '❌ Bekor qilish':
        await state.clear()
        user, is_registered = await check_user_registration(message.from_user.id)
        await message.answer("❌ Bekor qilindi", reply_markup=main_menu(is_registered))
        return
    
    # Barcha ma'lumotlarni olish
    data = await state.get_data()
    data['occupation'] = message.text
    
    # Database ga saqlash
    user = await update_user_data(
        message.from_user.id,
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        age=data['age'],
        occupation=data['occupation'],
        is_registered=True
    )
    
    await state.clear()
    
    await message.answer(
        "✅ Ro'yxatdan muvaffaqiyatli o'tdingiz!\n\n"
        f"👤 {data['first_name']} {data['last_name']}\n"
        f"📱 {data['phone']}\n"
        f"🎂 {data['age']} yosh\n"
        f"💼 {data['occupation']}\n\n"
        "Endi barcha imkoniyatlardan foydalanishingiz mumkin!",
        reply_markup=main_menu(True)
    )
