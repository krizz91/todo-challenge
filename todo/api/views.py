from datetime import datetime
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from ..models import Tasks
from .. import serializers

class TaskListView(GenericAPIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
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
            'data': serializedTasks.data
            }, status=status.HTTP_200_OK)

class CreateTask(GenericAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = (serializers.TasksSerializer)

    def post(self, request, *args, **kwargs):
        # try:
            task_data = serializers.TasksSerializer(data=request.data)
            task_data.is_valid(raise_exception=True)

            new_task = Tasks()
            new_task.description = task_data.validated_data['description']
            new_task.save()
            
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        # except Exception as e:
        #     return Response({}, status=status.HTTP_400_BAD_REQUEST)

class CompleteTask(GenericAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = (serializers.CompleteTaskSerializer)

    def post(self, request, *args, **kwargs):
        task_data = serializers.CompleteTaskSerializer(data=request.data)
        task_data.is_valid(raise_exception=True)

        # try:
        task = Tasks.objects.get(id=task_data.validated_data['id'])
        task.complete()
        
        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        # except Exception as e:
        #     return Response({
        #          "error": "Wrong ID provided"
        #         }, status=status.HTTP_400_BAD_REQUEST)
