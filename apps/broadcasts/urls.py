from django.urls import path
from . import views

app_name = 'broadcasts'

urlpatterns = [
    path('', views.broadcast_list, name='list'),
    path('create/', views.broadcast_create, name='create'),
    path('<int:pk>/', views.broadcast_detail, name='detail'),
    path('<int:pk>/delete/', views.broadcast_delete, name='delete'),
]
