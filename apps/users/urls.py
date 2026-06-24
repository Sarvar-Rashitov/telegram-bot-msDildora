from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='detail'),
    path('users/<int:pk>/edit/', views.user_edit, name='edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='delete'),
    path('users/<int:pk>/add-balance/', views.user_add_balance, name='add_balance'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='users:login'), name='logout'),
]
