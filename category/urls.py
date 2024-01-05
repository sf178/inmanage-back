from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('personal/', PersonalExpenseCategoryListCreateView.as_view(), name='personal-category-list'),
    # path('asset/', AssetCategoryListCreateView.as_view(), name='asset-category-list'),
    # path('liability/', LiabilityCategoryListCreateView.as_view(), name='liability-category-list'),
    # path('general/', ExpenseGeneralCategoryListView.as_view(), name='general-category-list'),
    # path('general/delete/<int:pk>/', ExpenseGeneralCategoryDeleteView.as_view(), name='general-category-delete'),
    # path('general/subcategories/delete/<int:pk>/', ExpenseGeneralSubcategoryDeleteView.as_view(), name='delete-general-subcategory'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
