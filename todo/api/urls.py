from django.urls import path
from .views import TaskListView, CreateTask, CompleteTask

urlpatterns = [
    path('list/', view=TaskListView.as_view(), name='list_tasks'),
    path('create/', view=CreateTask.as_view(), name='create_task'),
    path('complete/', view=CompleteTask.as_view(), name='complete_task')
]