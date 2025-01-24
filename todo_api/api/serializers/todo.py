from rest_framework import serializers
from todo_api.models import Todo, TodoUserAssignment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TodoUserAssignmentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True, allow_null=False, required=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = TodoUserAssignment
        fields = ['user_id', 'user', 'role', 'assigned_at']


class TodoSerializer(serializers.ModelSerializer):
    assigned_users = TodoUserAssignmentSerializer(source='todouserassignment_set', many=True, read_only=True)

    class Meta:
        model = Todo
        fields = [
            'id', 'title', 'description', 'completed', 
            'due_date', 'priority', 'created_at', 'updated_at', 'assigned_users'
        ]