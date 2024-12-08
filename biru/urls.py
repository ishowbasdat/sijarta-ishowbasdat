from django.urls import path
from . import views

app_name = 'biru'

urlpatterns = [
    path('discount/', views.discount, name='discount'),
    path('api/discounts/', views.get_discounts, name='get_discounts'),
    path('api/buy-voucher/', views.buy_voucher, name='buy_voucher'),
    path('tombol/', views.button_testi, name='button_testi'),
    path('api/get-metode/', views.get_metode_bayar, name='metode_bayar'),

    path('api/get_testimoni/<str:worker_id>/', views.get_testimoni, name='get_worker_testimonials'),
    path('api/delete_testimoni/', views.delete_testimoni, name='delete_testimoni'),
    path('api/submit-testimoni/', views.submit_testimonial, name='submit_testimonial'),
]
