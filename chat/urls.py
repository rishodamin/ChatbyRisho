from django.urls import path 
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/<str:act>', views.home, name='home'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('checkview', views.checkview, name='checkview'),
    path('room/<str:room>', views.room, name='room'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('send', views.send, name='send')
]