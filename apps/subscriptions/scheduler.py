from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from datetime import timedelta
from .models import Subscription

def check_expiring_subscriptions():
    """Check and update expiring subscriptions"""
    now = timezone.now()
    week_later = now + timedelta(days=7)
    
    # Mark subscriptions as expiring if they expire within 7 days
    Subscription.objects.filter(
        status='active',
        end_date__lte=week_later,
        end_date__gt=now
    ).update(status='expiring')
    
    # Mark subscriptions as expired if they passed end_date
    Subscription.objects.filter(
        status__in=['active', 'expiring'],
        end_date__lt=now
    ).update(status='expired')
    
    print(f"Subscription check completed at {now}")

def start_scheduler():
    """Start background scheduler"""
    scheduler = BackgroundScheduler()
    
    # Check subscriptions every hour
    scheduler.add_job(
        check_expiring_subscriptions,
        'interval',
        hours=1,
        id='check_subscriptions',
        replace_existing=True
    )
    
    scheduler.start()
    print("Scheduler started")
