from django.urls import path, include
from .views import *

app_name = 'merah'

urlpatterns = [
    path('', mypay_info, name='mypay_info'),
    path('transaction/', mypay_transaction, name='mypay_transaction'),
    path('get-service-price/<uuid:service_id>/', get_service_price, name='get_service_price'),
    path('pekerjaan-jasa', pekerjaan_jasa, name='pekerjaan_jasa'),
    path('get-subkategori-jasa/<uuid:kategori_id>', get_subkategori_jasa, name='get_subkategori_jasa'),
    path('filter-pekerjaan-jasa/<uuid:kategori_id>/<uuid:subkategori_id>', filter_pekerjaan_jasa, name='filter_pekerjaan_jasa'),
    path('status-pekerjaan-jasa', status_pekerjaan_jasa, name='status_pekerjaan_jasa'),
    path('filter-status-pekerjaan-jasa/<str:nama_jasa>/<uuid:status_pesanan>', filter_status_pekerjaan_jasa, name='filter_status_pekerjaan_jasa'),
]