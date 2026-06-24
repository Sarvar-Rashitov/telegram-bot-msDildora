from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from apps.users.models import User
from apps.support.models import SupportTicket
from apps.bot.states import SupportTicketStates
from apps.bot.keyboards import cancel_keyboard, main_menu, help_contact_keyboard
from django.db import close_old_connections

@sync_to_async
def check_user_registration(telegram_id):
    close_old_connections()
    user = User.objects.filter(telegram_id=telegram_id).first()
    return user, user.is_registered if user else False

@sync_to_async
def get_contact_info_text():
    """Yordam kontaktlarini olish"""
    close_old_connections()
    from apps.bot.models import ContactInfo
    
    contacts = ContactInfo.objects.filter(is_active=True).order_by('order')
    
    if not contacts:
        return None
    
    text = "📞 Yordam bo'limi\n\n"
    text += "Biz bilan bog'lanish:\n\n"
    
    for contact in contacts:
        icon = {
            'phone': '📱',
            'telegram': '✈️',
            'email': '📧',
            'other': '🔗'
        }.get(contact.contact_type, '📌')
        
        text += f"{icon} {contact.title}: {contact.value}\n"
    
    return text

async def cmd_help(message: Message):
    """Yordam kontaktlari + Murojaat inline tugma"""
    text = await get_contact_info_text()
    
    if not text:
        text = (
            "📞 Yordam bo'limi\n\n"
            "Savollaringiz bo'lsa, murojaat qoldiring."
        )
    
    await message.answer(
        text + "\n\n💬 Yoki murojaat qoldiring:",
        reply_markup=help_contact_keyboard()
    )

async def handle_create_ticket_callback(callback: CallbackQuery, state: FSMContext):
    """Murojaat qoldirish - Inline callback"""
    await callback.answer()
    await cmd_create_ticket(callback.message, state)

async def cmd_create_ticket(message: Message, state: FSMContext):
    """Murojaat qoldirish boshlash"""
    await state.set_state(SupportTicketStates.waiting_for_subject)
    await message.answer(
        "✍️ Murojaat qoldirish\n\n"
        "Murojaatingiz mavzusini kiriting:",
        reply_markup=cancel_keyboard()
    )

async def process_ticket_subject(message: Message, state: FSMContext):
    """Murojaat mavzusini qabul qilish"""
    if message.text == '❌ Bekor qilish':
        await state.clear()
        user, is_registered = await check_user_registration(message.from_user.id)
        await message.answer("❌ Bekor qilindi", reply_markup=main_menu(is_registered))
        return
    
    await state.update_data(subject=message.text)
    await state.set_state(SupportTicketStates.waiting_for_message)
    await message.answer(
        "Murojaatingizni batafsil yozing:",
        reply_markup=cancel_keyboard()
    )

@sync_to_async
def create_support_ticket(telegram_id, subject, message_text):
    close_old_connections()
    user = User.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return False
    
    SupportTicket.objects.create(
        user=user,
        subject=subject,
        message=message_text
    )
    return True

async def process_ticket_message(message: Message, state: FSMContext):
    """Murojaat matnini qabul qilish va saqlash"""
    if message.text == '❌ Bekor qilish':
        await state.clear()
        user, is_registered = await check_user_registration(message.from_user.id)
        await message.answer("❌ Bekor qilindi", reply_markup=main_menu(is_registered))
        return
    
    data = await state.get_data()
    subject = data.get('subject', 'Murojaat')
    
    success = await create_support_ticket(message.from_user.id, subject, message.text)
    
    await state.clear()
    user, is_registered = await check_user_registration(message.from_user.id)
    
    if success:
        await message.answer(
            "✅ Murojaatingiz qabul qilindi!\n\n"
            "Tez orada admin javob beradi.",
            reply_markup=main_menu(is_registered)
        )
    else:
        await message.answer(
            "❌ Xatolik yuz berdi. /start bosib qaytadan urinib ko'ring.",
            reply_markup=main_menu(is_registered)
        )
