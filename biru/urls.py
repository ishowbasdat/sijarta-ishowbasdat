from django.urls import path
from . import views

app_name = 'biru'

urlpatterns = [
    path('discount/', views.discount, name='discount'),
    path('api/discounts/', views.get_discounts, name='get_discounts'),
    path('api/buy-voucher/', views.buy_voucher, name='buy_voucher'),
    path('tombol/', views.button_testi, name='button_testi')
]