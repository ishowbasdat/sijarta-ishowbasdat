from django.urls import path, include
from .views import *

app_name = 'merah'

urlpatterns = [
    path('', mypay_info, name='mypay_info'),
    path('transaction/', mypay_transaction, name='mypay_transaction'),
]
