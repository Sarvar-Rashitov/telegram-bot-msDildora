from aiogram.types import Message
from asgiref.sync import sync_to_async
from apps.subscriptions.models import Tariff
from apps.bot.keyboards import tariff_menu

@sync_to_async
def get_active_tariffs():
    return list(Tariff.objects.filter(is_active=True))

async def cmd_subscribe(message: Message):
    tariffs = await get_active_tariffs()
    
    if not tariffs:
        await message.answer("❌ Hozirda mavjud tariflar yo'q.")
        return
    
    text = "💳 Obuna tariflari:\n\n"
    for tariff in tariffs:
        text += f"📦 {tariff.name}\n"
        text += f"💰 Narx: {tariff.price} so'm\n"
        text += f"📅 Muddat: {tariff.duration_days} kun\n"
        text += f"📝 {tariff.description}\n\n"
    
    await message.answer(text, reply_markup=tariff_menu(tariffs))
