from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('stats/', views.get_stats, name='stats'),
    path('users/', views.get_users, name='users'),
    path('subscriptions/', views.get_subscriptions, name='subscriptions'),
]
