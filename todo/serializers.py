from rest_framework import serializers

from todo.models import Tasks

class TasksSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=True)

    class Meta:
        model = Tasks
        fields = ('id', 'description', 'created', 'completed')
        read_only_fields = ('id', 'description', 'created', 'completed')

class CompleteTaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)

    def validate_id(self, value):
        if not Tasks.objects.filter(id=value, completed=False).exists():
            raise serializers.ValidationError("Wrong ID. You have to provide a valid ID")
        return value
