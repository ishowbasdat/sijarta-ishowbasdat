from django.urls import path
from . import views

app_name = 'testi_diskon_pbvoucher'

urlpatterns = [
    path('', views.show_main, name='main'),
]