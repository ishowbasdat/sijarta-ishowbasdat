from .views import homepage, subkategori, get_metode_pembayaran, create_order, pesanan, cancel_pesanan
from django.urls import path

app_name = 'hijau'

urlpatterns = [
    path('', homepage, name='homepage'),
    path('subkategori/<str:id>', subkategori, name='subkategori'),
    path('api/get-metode-pembayaran/', get_metode_pembayaran, name='get_metode_pembayaran'),
    path('api/create-order/', create_order, name='create_order'),
    path('pesanan/', pesanan, name='pesanan'),
    path('cancel-pesanan/<str:id>', cancel_pesanan, name='cancel_pesanan')
]

