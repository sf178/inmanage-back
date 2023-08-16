from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('personal/', ExpensePersonalCategoryListView.as_view(), name='personal-category-list'),
    path('general/', ExpenseGeneralCategoryListView.as_view(), name='general-category-list')


]

urlpatterns = format_suffix_patterns(urlpatterns)
