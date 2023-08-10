from django.urls import path
from .views import *

urlpatterns = [
    path('tasks/', TodoTaskListView.as_view(), name='todo-task-list'),
    path('tasks/<int:id>/', TodoTaskDetailView.as_view(), name='todo-task-detail'),
    path('tasks/del/<int:pk>/', TodoTaskDeleteView.as_view(), name='todo-task-delete'),
    path('items/', TodoItemListView.as_view(), name='todo-item-list'),
    path('items/<int:id>/', TodoItemDetailView.as_view(), name='todo-item-detail'),
    path('items/del/<int:pk>/', TodoItemDeleteView.as_view(), name='todo-item-delete'),
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/<int:id>/', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/del/<int:pk>/', ProjectDeleteView.as_view(), name='project-delete'),
    path('', PlannerListView.as_view(), name='planner-list')
]