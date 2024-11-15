from .views import homepage, get_json_from_query
from django.urls import path

app_name = 'hijau'

urlpatterns = [
    path('', homepage, name='homepage'),
    path('get_json_from_query/<str:query>', get_json_from_query, name='get_json_from_query'),
]