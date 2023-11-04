# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReceiptView.as_view(), name='list-receipts'),
    path('<int:pk>/', views.DeleteReceiptView.as_view(), name='delete-receipt'),
]
