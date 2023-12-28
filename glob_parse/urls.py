
from django.urls import path
from views import start_parsing

urlpatterns = [
    path('parse/', start_parsing, name='parse_avito'),
]