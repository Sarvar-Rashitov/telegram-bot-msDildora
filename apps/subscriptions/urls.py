from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('', views.subscription_list, name='subscription_list'),
    path('<int:pk>/', views.subscription_detail, name='subscription_detail'),
    path('<int:pk>/activate/', views.subscription_activate, name='subscription_activate'),
    path('<int:pk>/cancel/', views.subscription_cancel, name='subscription_cancel'),
    
    path('tariffs/', views.tariff_list, name='tariff_list'),
    path('tariffs/create/', views.tariff_create, name='tariff_create'),
    path('tariffs/<int:pk>/edit/', views.tariff_edit, name='tariff_edit'),
    path('tariffs/<int:pk>/delete/', views.tariff_delete, name='tariff_delete'),
    
    path('promo/', views.promo_list, name='promo_list'),
    path('promo/create/', views.promo_create, name='promo_create'),
    path('promo/<int:pk>/edit/', views.promo_edit, name='promo_edit'),
    path('promo/<int:pk>/toggle/', views.promo_toggle, name='promo_toggle'),
    path('promo/<int:pk>/delete/', views.promo_delete, name='promo_delete'),
]
