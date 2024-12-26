from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
     path('home/', views.home, name='home'),
    path('register/', views.user_register, name='user_register'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('send_message/<int:user_id>/', views.send_message, name='send_message_with_user'),  
     path('send_message_to_santa/', views.send_message_to_santa, name='send_message_to_santa'), #Santa_message
    path('send_message/', views.send_message, name='send_message'),
    path('logout/', views.user_logout, name='user_logout'),
]
