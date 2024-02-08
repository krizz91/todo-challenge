from datetime import datetime
from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import serializers as drf_serializers

from todo import serializers
from todo.models import Tasks

class LoginView(GenericAPIView):

    permission_classes = (AllowAny, )
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        serializer = self.get_serializer(data={'username': username,
                                               'password': password})

        try:
            if not serializer.is_valid():
                response = Response({"status": "failed",
                                     "message": serializer.errors},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                user = serializer.validated_data['user']
                login(self.request, user)

                response = Response({
                    "status": "success"
                    }, status=status.HTTP_200_OK)
        except Exception as e:
            response = Response({"status": "failed",
                                 "message": e},
                                status=status.HTTP_200_OK)
        return response


class LogoutView(GenericAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = drf_serializers.Serializer

    def post(self, request, *args, **kwargs):
        logout(self.request)
        return Response({"status": "success",
                         "message": "Successfully logged out."},
                        status=status.HTTP_200_OK)

class TaskListView(GenericAPIView):
    """
    This view's main target is the representation of the tasks

    Method:
    - get: This method manage the GET requests, returning a list of Tasks. You can filter by description and date (date_lte for lower than and date_gte gor greater than) and you can order by date (order_asc and order_desc)

    Parameters:
    - description (optional): ''
    - date_lte (optional): 'dd-mm-YYYY'
    - date_gte (optional): 'dd-mm-YYYY'
    - order_asc (optional): True/False
    - order_desc (optional): True/False
    """

    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        """
        This function return a list of tasks. This function can filter the list of tasks too

        Parameters:
        - description (optional)
        - date_lte (optional)
        - date_gte (optional)
        - order_asc (optional)
        - order_desc (optional)
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
        order_asc = request.GET.get('order_asc', False)
        order_desc = request.GET.get('order_desc', False)
        if order_asc and order_desc:
            return Response({
                'data': 'You only can set one order value',
                'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)
        if(order_asc):
            tasks = tasks.order_by('created')
        if(order_desc):
            tasks = tasks.order_by('-created')

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
    serializer_class = serializers.TasksSerializer

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
    serializer_class = serializers.CompleteTaskSerializer

    def post(self, request, *args, **kwargs):
        """
        This function mark a task by completed

        Parameters:
        - id (mandatory)
        """
        serializer = self.get_serializer(data=request.data)
        try:
            if not serializer.is_valid():
                response = Response({"status": "failed",
                                     "message": serializer.errors},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                task_data = serializers.CompleteTaskSerializer(data=request.data)
                task_data.is_valid(raise_exception=True)

                task = Tasks.objects.get(id=task_data.validated_data['id'])
                task.complete()
                
                response = Response({
                    'status': 'success'
                    }, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = Response({"status": "failed",
                                 "message": e},
                                status=status.HTTP_200_OK)
        return response
