# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReceiptAPI.as_view(), name='list-receipts'),
]
