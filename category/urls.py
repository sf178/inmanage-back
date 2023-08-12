from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('', ExpenseCategoryListView.as_view(), name='category-list'),


]

urlpatterns = format_suffix_patterns(urlpatterns)
