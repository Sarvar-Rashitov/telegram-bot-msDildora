from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.payment_list, name='list'),
    path('<int:pk>/', views.payment_detail, name='detail'),
    path('export/', views.payment_export, name='export'),
    path('click/prepare/', views.click_prepare, name='click_prepare'),
    path('click/complete/', views.click_complete, name='click_complete'),
]
