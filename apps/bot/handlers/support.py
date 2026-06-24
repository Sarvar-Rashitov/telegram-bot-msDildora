from aiogram.types import Message
from asgiref.sync import sync_to_async
from apps.users.models import User
from apps.support.models import SupportTicket

async def cmd_support(message: Message):
    text = (
        "📞 Yordam bo'limi\n\n"
        "Savolingizni yoki murojaatingizni yuboring.\n"
        "Tez orada admin javob beradi."
    )
    await message.answer(text)

@sync_to_async
def create_support_ticket(telegram_id, text):
    user = User.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return False
    
    SupportTicket.objects.create(
        user=user,
        subject="Support request",
        message=text
    )
    return True

async def handle_support_message(message: Message):
    success = await create_support_ticket(message.from_user.id, message.text)
    
    if success:
        await message.answer("✅ Murojaatingiz qabul qilindi. Tez orada javob beramiz.")
    else:
        await message.answer("❌ Xatolik yuz berdi. /start bosib qaytadan urinib ko'ring.")
