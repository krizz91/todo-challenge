from datetime import datetime
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from todo import serializers
from todo.models import Tasks

class TaskListView(GenericAPIView):
    """
    This view's main target is the representation of the tasks

    Method:
    - get: This method manage the GET requests, returning a list of Tasks.
    You can filter by description and by date (date_lte for lower than and date_gte gor greater than)
    """

    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        """
        This function return a list of tasks. This function can filter the list of tasks too

        Parameters:
        - description (optional)
        - date_lte (optional)
        - date_gte (optional)
        """
        tasks = Tasks.objects.all()

        description = request.GET.get('description', None)
        if(description):
            tasks = tasks.filter(description__icontains=description)
        date_lte = request.GET.get('date_lte', None)
        if(date_lte):
            date_lte = datetime.strptime(date_lte, '%d-%m-%Y')
            tasks = tasks.filter(created__lte=date_lte)
        date_gte = request.GET.get('date_gte', None)
        if(date_gte):
            date_gte = datetime.strptime(date_gte, '%d-%m-%Y')
            tasks = tasks.filter(created__gte=date_gte)
        
        serializedTasks = serializers.TasksSerializer(tasks, many=True)
        return Response({
            'data': serializedTasks.data,
            'status': 'success'
            }, status=status.HTTP_200_OK)

class CreateTask(GenericAPIView):
    """
    This view's main target is the creation of the tasks

    Method:
    - post: This method manage the POST requests.
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = (serializers.TasksSerializer)

    def post(self, request, *args, **kwargs):
        """
        This function allows the user create a new task. This new task is created with the completed flag in false

        Parameters:
        - description (mandatory)
        """
        task_data = serializers.TasksSerializer(data=request.data)
        task_data.is_valid(raise_exception=True)

        new_task = Tasks()
        new_task.description = task_data.validated_data['description']
        new_task.save()
        
        return Response({
            'status': 'success'
            }, status=status.HTTP_201_CREATED)

class CompleteTask(GenericAPIView):
    """
    This view's main target is to provide a way to complete tasks

    Method:
    - post: This method manage the POST requests.
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = (serializers.CompleteTaskSerializer)

    def post(self, request, *args, **kwargs):
        """
        This function mark a task by completed

        Parameters:
        - id (mandatory)
        """
        task_data = serializers.CompleteTaskSerializer(data=request.data)
        task_data.is_valid(raise_exception=True)

        task = Tasks.objects.get(id=task_data.validated_data['id'])
        task.complete()
        
        return Response({
            'status': 'success'
            }, status=status.HTTP_201_CREATED)
