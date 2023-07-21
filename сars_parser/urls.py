from django.urls import path
from .views import *


urlpatterns = [
    path('cars/', CarListCreateAPIView.as_view(), name='car-list-create'),
    path('cars/<int:pk>/', CarRetrieveUpdateDestroyAPIView.as_view(), name='car-retrieve-update-destroy'),
]
