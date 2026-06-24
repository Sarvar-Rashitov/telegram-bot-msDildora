from aiogram.types import Message, FSInputFile
from asgiref.sync import sync_to_async
from apps.bot.models import BotSettings, BotInfo
from django.db import close_old_connections
import os

@sync_to_async
def get_license_file():
    close_old_connections()
    setting = BotSettings.objects.filter(key='license_file').first()
    if setting and setting.file:
        return setting.file.path
    return None

@sync_to_async
def get_bot_info():
    close_old_connections()
    info_items = BotInfo.objects.filter(is_active=True).order_by('order')
    return list(info_items)

async def cmd_license(message: Message):
    """Litsenziya PDF faylni yuborish"""
    file_path = await get_license_file()
    
    if not file_path or not os.path.exists(file_path):
        await message.answer(
            "❌ Litsenziya fayli topilmadi.\n"
            "Iltimos, admin bilan bog'laning."
        )
        return
    
    try:
        document = FSInputFile(file_path)
        await message.answer_document(
            document=document,
            caption="📄 Litsenziya shartnomasi"
        )
    except Exception as e:
        await message.answer("❌ Faylni yuborishda xatolik yuz berdi.")

async def cmd_info(message: Message):
    """Bot haqida ma'lumotlar"""
    info_items = await get_bot_info()
    
    if not info_items:
        await message.answer(
            "ℹ️ Ma'lumot\n\n"
            "Bot haqida ma'lumot hozircha qo'shilmagan."
        )
        return
    
    for info in info_items:
        text = f"📌 {info.title}\n\n{info.content}"
        
        if info.image:
            try:
                photo = FSInputFile(info.image.path)
                await message.answer_photo(photo=photo, caption=text)
            except:
                await message.answer(text)
        else:
            await message.answer(text)
