from django.urls import path
from .views import WorkIncomeListView, WorkIncomeDetailView, WorkIncomeCreateView, WorkListView, WorkDetailView, ProjectListView, ProjectDetailView

urlpatterns = [
    # Маршруты для WorkIncome
    path('', WorkIncomeListView.as_view(), name='workincome-list'),
    path('<int:pk>/', WorkIncomeDetailView.as_view(), name='workincome-detail'),
    path('create/', WorkIncomeCreateView.as_view(), name='workincome-create'),

    # Маршруты для Work
    path('works/', WorkListView.as_view(), name='work-list'),
    path('works/<int:pk>/', WorkDetailView.as_view(), name='work-detail'),

    # Маршруты для Project
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
]
