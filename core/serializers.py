from rest_framework import serializers
from .models import Project, Task, Team
from django.contrib.auth.models import User


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Project

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Task

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'id', 'sequence', 'status', 'd_tasks', 'assigned_to', 'completion_time', 'start_date')
        model = Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('password', )
        model = User

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('members', )
        model = Team



