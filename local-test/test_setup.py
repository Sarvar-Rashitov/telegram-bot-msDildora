"""
Test script to verify Django setup
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User
from apps.subscriptions.models import Tariff

print("Testing Django setup...")

# Create test tariff
tariff = Tariff.objects.create(
    name="Bir oylik",
    description="30 kunlik obuna",
    price=50000,
    duration_days=30
)
print(f"✅ Created tariff: {tariff}")

# List all tariffs
tariffs = Tariff.objects.all()
print(f"✅ Total tariffs: {tariffs.count()}")

print("\n✅ Django setup is working correctly!")
print("\nNext steps:")
print("1. Edit .env file with your bot token and credentials")
print("2. Run: python manage.py runserver")
print("3. Run: python manage.py runbot")
