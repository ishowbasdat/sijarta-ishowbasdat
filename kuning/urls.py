from django.urls import path
from .views import landing, login, register, logout, profile

app_name = 'kuning'

urlpatterns = [
    path('', landing, name='landing'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile')
]