from django.urls import path
from .views import landing

app_name = 'kuning'

urlpatterns = [
    path('', landing, name='landing'),
]