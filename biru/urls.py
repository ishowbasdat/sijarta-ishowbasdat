from django.urls import path
from . import views

app_name = 'biru'

urlpatterns = [
    path('', views.show_main, name='main'),
    #path('', views.discount, name='discount')
]