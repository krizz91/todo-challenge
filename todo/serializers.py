from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from todo.models import Tasks


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            try:
                usr = User.objects.get(username=username)
            except Exception as e:
                msg = _('Credentials are invalid.')
                raise ValidationError(msg)
            user = authenticate(username=username, password=password)

        else:
            msg = _('Must include "username" and "password".')
            raise ValidationError(msg)

        if not user or not user.is_active:
            msg = _('Credentials are invalid.')
            raise ValidationError(msg)

        attrs['user'] = user
        return attrs

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
            msg = _('Wrong ID. You have to provide a valid ID')
            raise ValidationError(msg)
        return value
