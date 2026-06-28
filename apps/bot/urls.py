from django.urls import path
from . import views

app_name = 'bot'

urlpatterns = [
    path('webhook/', views.telegram_webhook, name='telegram_webhook'),
    
    path('settings/', views.bot_settings_list, name='settings_list'),
    path('settings/<int:pk>/edit/', views.bot_settings_edit, name='settings_edit'),
    
    path('contacts/create/', views.contact_create, name='contact_create'),
    path('contacts/<int:pk>/edit/', views.contact_edit, name='contact_edit'),
    path('contacts/<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    
    path('info/create/', views.info_create, name='info_create'),
    path('info/<int:pk>/edit/', views.info_edit, name='info_edit'),
    path('info/<int:pk>/delete/', views.info_delete, name='info_delete'),
]
