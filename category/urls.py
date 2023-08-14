from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('personal/', ExpenseCategoryListView.as_view(), name='personal-category-list'),


]

urlpatterns = format_suffix_patterns(urlpatterns)
