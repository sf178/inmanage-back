from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('personal', ExpensePersonalCategoryListView.as_view(), name='personal-category-list'),
    path('personal/delete/<int:pk>/', ExpensePersonalCategoryDeleteView.as_view(), name='personal-category-delete'),

    path('general', ExpenseGeneralCategoryListView.as_view(), name='general-category-list'),
    path('general/delete/<int:pk>/', ExpenseGeneralCategoryDeleteView.as_view(), name='general-category-delete'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
