from django.contrib import admin
from django.urls import path, include
from .views import TaskManagerView, TaskManagerDetailsView

urlpatterns = [
    path('tasks/', TaskManagerView.as_view()),
    path('task_details/', TaskManagerDetailsView.as_view())
]
