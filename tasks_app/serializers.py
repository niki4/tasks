from rest_framework import serializers

from tasks_app.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('task_name')
