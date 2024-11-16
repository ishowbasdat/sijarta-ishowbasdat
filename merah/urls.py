from django.urls import path, include
from .views import *

app_name = 'merah'

urlpatterns = [
    path('', mypay_info, name='mypay_info'),
    path('transaction/', mypay_transaction, name='mypay_transaction'),
    path('pekerjaan-jasa', pekerjaan_jasa, name='pekerjaan_jasa'),
    path('status-pekerjaan-jasa', status_pekerjaan_jasa, name='status_pekerjaan_jasa')
]
