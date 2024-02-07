from django.urls import path
from .views import TaskListView, CreateTask, CompleteTask, LoginView, LogoutView

urlpatterns = [
    path('login/', view=LoginView.as_view(), name='login'),
    path('logout/', view=LogoutView.as_view(), name='logout'),
    path('list/', view=TaskListView.as_view(), name='list_tasks'),
    path('create/', view=CreateTask.as_view(), name='create_task'),
    path('complete/', view=CompleteTask.as_view(), name='complete_task')
]